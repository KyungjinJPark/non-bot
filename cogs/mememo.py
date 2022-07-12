import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

import json
import os
import importlib
from helpers.gen import respond, temp_send, temp_reply
guild_ids = importlib.import_module('non-only.env').DC_GUILDS.values()


################################
#  Json Helpers                #
################################

fp = os.path.join(os.path.dirname(__file__), '../non-only/mememos.json')
def get_mememo_keys():
    with open(fp, 'r') as f:
        data = json.load(f)
    return data.keys()
def get_mememo(key):
    with open(fp, 'r') as f:
        data = json.load(f)
    return data[key]
def update_mememo(key, val):
    with open(fp, 'r+') as f:
        data = json.load(f)
        data[key] = val
        json.dump(data, f)
def delete_mememo(key):
    with open(fp, 'r+') as f:
        data = json.load(f)
        del data[key]
        json.dump(data, f)

################################


class Mememo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        '''On cog load'''
        print(f'{__class__.__name__} cog is ready!')


    ################################
    #  User Commands               #
    ################################

    # @cog_ext.cog_slash(
    #     description='Tell non bot to remember the message you are replying to and associate it with a name',
    #     options=[
    #         create_option(
    #             name='memory',
    #             description='The memory name to remember.',
    #             option_type=SlashCommandOptionType.STRING,
    #             required=True,
    #         )
    #     ],
    #     guild_ids=guild_ids
    # )
    @commands.command()
    async def memo(self, ctx, memory: str):
        if ctx.message.reference == None:
            await temp_send(ctx, f'Please reply to the message you want me to memorize!')
            return
        memsg_id = ctx.message.reference.message_id
        
        if memory in get_mememo_keys():
            await temp_send(ctx, f'I already memorize something else as `{memory}`!')
            return

        update_mememo(memory, memsg_id)
        memsg = await ctx.channel.fetch_message(memsg_id)
        await temp_reply(memsg, f'I will remember this message as `{memory}`!', False)
    
    @cog_ext.cog_slash(
        description='Tell non bot to recall a message associated with a name',
        options=[
            create_option(
                name='memory',
                description='The memory name to recall',
                option_type=SlashCommandOptionType.STRING,
                required=True,
            )
        ],
        guild_ids=guild_ids
    )
    async def recall(self, ctx, memory):
        recall_msg = await ctx.channel.fetch_message(get_mememo(memory))

        files = []
        for attachment in recall_msg.attachments:
            files.append(await attachment.to_file(spoiler=attachment.is_spoiler()))
        await respond(ctx, f'aauuhh')
        await recall_msg.reply(f'I remember `{memory}`!\n{recall_msg.content}', files=files, mention_author=False)

    @cog_ext.cog_slash(
        description='Tell non bot to forget the message associated with a name',
        options=[
            create_option(
                name='memory',
                description='The memory name to recall',
                option_type=SlashCommandOptionType.STRING,
                required=True,
            )
        ],
        guild_ids=guild_ids
    )
    async def forget(self, ctx, memory):     
        if memory not in get_mememo_keys():
            await temp_send(ctx, f'I never remembered a `{memory}`!')
            return

        delete_mememo(memory)
        await temp_send(ctx, f'I don\'t remember `{memory}` anymore...')

    @cog_ext.cog_slash(description='Tell non bot to list everything it remembers', guild_ids=guild_ids)
    async def list(self, ctx):
        mems = get_mememo_keys()
        if not mems:
            await respond(ctx, f'I remember nothing...')
            return

        format = ''
        for memory in list(mems):
            format += f'`{memory}`, '
        await respond(ctx, f'I remember these: {format[:-2]}')


def setup(bot):
    bot.add_cog(Mememo(bot))
