import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

import importlib  
guild_ids = importlib.import_module('non-only.env').DC_GUILDS.values()


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        '''On cog load'''
        print(f'{__class__.__name__} cog is ready!')


    ################################
    #  Error Handlers              #
    ################################

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """ # this is apparently how to document? idk I stole it from the docs
        
        if isinstance(error, commands.CommandNotFound):
            err_cmd = str(error).split('"')[1]
            await ctx.send(f'`{err_cmd}` is not a command I recognize.')
            # print(dir(error))
            # print(dir(error.args))
            # print([x for x in error.args])
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You are missing required arguments `{error.param}`.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You don\'t have sufficient permissions to do that.')
        else:
            await ctx.send(f'Some... error happened... No handler for this one. Error dump:\n```\n{error}\n```')
            print(f'UNHANDLED ERROR > {error}')

    @cog_ext.cog_slash(description='throw an error',
                        options=[
                            create_option(
                                name='error',
                                description='True: Discord Error; False: Assertion Error',
                                option_type=SlashCommandOptionType.BOOLEAN,
                                required=True,
                            )
                        ],
                        guild_ids=guild_ids)
    async def err(self, ctx: SlashContext, error: bool):
        if error:
            print('Discord Error')
            raise discord.DiscordException()
        else:
            print('Assertion Error')
            raise AssertionError()


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
