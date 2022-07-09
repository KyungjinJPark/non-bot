import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType


# Helper commands
DELETE_DELAY = 5
async def temp_send(ctx, msg):
    await ctx.send(msg, delete_after=DELETE_DELAY)
async def temp_reply(orig, msg, mention):
    await orig.reply(msg, mention_author=mention, delete_after=DELETE_DELAY)

def get_mememo(key):
  return db[key]
def update_mememo(key, val):
  db[key] = val
def delete_mememo(key):
  del db[key]
def mememo_keys():
  return db.keys()

class Mememo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    On cog load
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__class__.__name__} cog is ready!')


    ################################
    #  User Commands               #
    ################################

    guild_ids = [000000000000000000, 000000000000000000]
    
    @cog_ext.cog_slash(description='Tell Non to remember the message you are replying to and associate it with a name',
                        options=[
                            create_option(
                                name='memory',
                                description='The memory name to remember.',
                                option_type=SlashCommandOptionType.STRING,
                                required=True,
                            )
                        ],
                        guild_ids=guild_ids)
    async def memo(self, ctx, memory: str):
        if ctx.message.reference == None:
            await temp_send(ctx, f'Reply to the message you want me to memorize!')
            return
        memsg_id = ctx.message.reference.message_id
        
        if memory in mememo_keys():
            await temp_send(ctx, f'I already memorize something else as `{memory}`!')
            return
        update_mememo(memory, memsg_id)

        memsg = await ctx.channel.fetch_message(memsg_id)
        await temp_reply(memsg, f'I will remember this message as `{memory}`!', False)
    
    @cog_ext.cog_slash(description='Tell Non to recall a message associated with a name',
                        options=[
                            create_option(
                                name='memory',
                                description='The memory name to recall.',
                                option_type=SlashCommandOptionType.STRING,
                                required=True,
                            )
                        ],
                        guild_ids=guild_ids)
    async def recall(self, ctx, memory):
        recall_msg = await ctx.channel.fetch_message(get_mememo(memory))

        files = []
        for attachment in recall_msg.attachments:
            files.append(await attachment.to_file(spoiler=attachment.is_spoiler()))
        await recall_msg.reply(f'I remember `{memory}`!\n{recall_msg.content}', files=files, mention_author=False)

    @cog_ext.cog_slash(description='Tell Non to forget the message associated with a name',
                        options=[
                            create_option(
                                name='memory',
                                description='The memory name to recall.',
                                option_type=SlashCommandOptionType.STRING,
                                required=True,
                            )
                        ],
                        guild_ids=guild_ids)
    async def forget(self, ctx, memory):     
        if memory not in mememo_keys():
            await temp_send(ctx, f'I don\'t remmeber a `{memory}`!')
            return
        delete_mememo(memory)

        await temp_send(ctx, f'I don\'t remember `{memory}` anymore...')

    @cog_ext.cog_slash(description='Tell Non to list everything it remembers', guild_ids=guild_ids)
    async def list(self, ctx):
        if not mememo_keys():
            await ctx.send(f'I remember nothing...')
            return

        format = ''
        for memory in list(mememo_keys()):
            format += f'`{memory}`, '
        await ctx.send(f'I remember these: {format[:-2]}')


def setup(bot):
    pass
    # bot.add_cog(Mememo(bot))
