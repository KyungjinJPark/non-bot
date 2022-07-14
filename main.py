import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

import os
from helpers.gen import respond, guild_ids


# Bot inits
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='non ', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    '''On bot load'''
    print(f'Logged on as \'{bot.user}\'!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('\'non help\' for help'))


################################
#  Cog Loading                 #
################################

def get_all_cogs():
    '''Populate a list of cogs'''
    cogs_list=[]
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs_list.append(filename[:-3])
    return cogs_list

def load_all_cogs(cogs_list):
    '''Load a list of cogs'''
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')

# Initial load of cogs
cogs_list = get_all_cogs()
load_all_cogs(cogs_list)

@slash.slash(
    name='listAvailableCogs',
    description='Get all available extensions',
    guild_ids=guild_ids
)
async def list_available_cogs(ctx: SlashContext):
    await respond(ctx, str(get_all_cogs()))

@slash.slash(
    description='Load an extension',
    options=[
        create_option(
            name='extension',
            description='The name of the extension to load',
            option_type=SlashCommandOptionType.STRING,
            required=True,
        )
    ],
    guild_ids=guild_ids
)
async def load(ctx: SlashContext, extension: str): # extension = cog to load
    try:
        bot.load_extension(f'cogs.{extension}')
    except:
        await respond(ctx, f'Error! Extension `{extension}` was **NOT** loaded!')
        return
    await respond(ctx, f'Extension `{extension}` loaded!')
    
# def list_current_extensions():
#     ext_list = []
#     for cog in bot.extensions.keys():
#         cog_name = cog[cog.find('.') + 1:]
#         ext_list.append(create_choice(
#             name=cog_name,
#             value=cog_name
#         ))
#     return ext_list

# TODO: The commands remain from the unloaded cog... Of course
@slash.slash(
    description='Unloads an extension',
    options=[
        create_option(
            name='extension',
            description='The name of the extension you want to unload',
            option_type=SlashCommandOptionType.STRING,
            required=True,
            # choices=list_current_extensions() # Confirmed this does not dynamically change option choices.
        )
    ],
    guild_ids=guild_ids
)
async def unload(ctx: SlashContext, extension: str):
    try:
        bot.unload_extension(f'cogs.{extension}')
    except:
        await respond(ctx, f'Error! Extension `{extension}` was **NOT** unloaded!')
        return
    await respond(ctx, f'Cog `{extension}` unloaded!')

def try_reload(ext):
    try:
        bot.reload_extension(ext)
        return True
    except:
        return False

@slash.slash(
    description='Reloads an extension. just `reload` or `reload -a` calls `reloadAll`',
    options=[
        create_option(
            name='extension',
            description='The name of the extension to reload',
            option_type=SlashCommandOptionType.STRING,
            required=False,
        )
    ],
    guild_ids=guild_ids
)
async def reload(ctx: SlashContext, extension: str='-a'):
    if extension == '-a':
        await reload_all(ctx)
        return
    if try_reload(f'cogs.{extension}'):
        await respond(ctx, f'Cog `{extension}` reloaded!')
    else:
        await respond(ctx, f'Error! Cog `{extension}` was **NOT** reloaded!')

@slash.slash(name='reloadAll', description='Reloads all extensions', guild_ids=guild_ids)
async def reload_all(ctx):
    for cog in bot.extensions.keys():
        if not try_reload(cog):
            await respond(ctx, f'Error! Extension `{cog[5:]}` was **NOT** reloaded!')
    await respond(ctx, f'Reload finished!')

################################


bot.run(os.getenv('DC_BOT_TOKEN'))
