import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

import os # TODO: should I just hardcode all my extensions?


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='non ', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

'''
On bot load
'''
@bot.event
async def on_ready():
    print(f'Logged on as \'{bot.user}\'!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Do \'non help\' for help'))


################################
#  Cog Loading                 #
################################

# TODO: get rid of this to make commands global
'''
Populate the list of cogs
'''
cogs_list=[]
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cogs_list.append(create_choice(
            name=filename[:-3],
            value=filename[:-3]
        ))

'''
Initial load of all cogs
'''
def loadAllCogs():
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog["value"]}')
loadAllCogs()


'''
Helper functions
'''
async def respond(ctx, msg):
    await ctx.send(msg)

@slash.slash(description='Loads an extension.',
            options=[
                create_option(
                    name='extension',
                    description='The name of the extension you want to load.',
                    option_type=SlashCommandOptionType.STRING,
                    required=True,
                    choices=cogs_list
                )
            ],
            guild_ids=guild_ids)
async def load(ctx: SlashContext, extension: str): # extension = cog to load
    try:
        bot.load_extension(f'cogs.{extension}')
    except:
        await respond(ctx, f'Error! Cog `{extension}` was **NOT** loaded!')
        return
    await respond(ctx, f'Cog `{extension}` loaded!')

# TODO: Confirmed this does not dynamically change option choices. ALSO tho, the commands remain from the unloaded cog... Of course
def extension_list():
    ext_list = []
    for cog in bot.extensions.keys():
        cog_name = cog[cog.find('.') + 1:]
        ext_list.append(create_choice(
            name=cog_name,
            value=cog_name
        ))
    return ext_list

@slash.slash(description='Unloads an extension.',
            options=[
                create_option(
                    name='extension',
                    description='The name of the extension you want to unload.',
                    option_type=SlashCommandOptionType.STRING,
                    required=True,
                    choices=extension_list()
                )
            ],
            guild_ids=guild_ids)
async def unload(ctx: SlashContext, extension:str):
    try:
        bot.unload_extension(f'cogs.{extension}')
    except:
        await respond(ctx, f'Error! Cog `{extension}` was **NOT** loaded!')
        return
    await respond(ctx, f'Cog `{extension}` unloaded!')

def try_reload(bot, ext):
    try:
        bot.reload_extension(ext)
        return True
    except:
        return False

async def reload_all(ctx):
    for cog in bot.extensions.keys():
        if not try_reload(bot, cog):
            await respond(ctx, f'Error! Cog `{cog[5:]}` was **NOT** reloaded!')
    await respond(ctx, f'Reload finished!')

@slash.slash(description='Reloads an extension. just `reload` or `reload -a` calls reload_all.',
            options=[
                create_option(
                    name='extension',
                    description='The name of the extension you want to reload.',
                    option_type=SlashCommandOptionType.STRING,
                    required=False,
                    choices=extension_list()
                )
            ],
            guild_ids=guild_ids)
async def reload(ctx: SlashContext, extension: str='-a'):
    if extension == '-a':
        await reload_all(ctx)
        return
    if try_reload(bot, f'cogs.{extension}'):
        await respond(ctx, f'Cog `{extension}` reloaded!')
    else:
        await respond(ctx, f'Error! Cog `{extension}` was **NOT** reloaded!')

@slash.slash(name='reload-all', description='Reloads all extensions.', guild_ids=guild_ids)
async def _reload_all(ctx):
    await reload_all(ctx)

################################

bot.run(os.environ['DC_BOT_TOKEN'])
