import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

import importlib  
from helpers.gen import respond
guild_ids = importlib.import_module('non-only.env').DC_GUILDS.values()


class Test(commands.Cog): # `Test` inherits from `commands.Cog`
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        '''On cog load'''
        print(f'{__class__.__name__} cog is ready!')


    ################################
    #  User Commands               #
    ################################

    @cog_ext.cog_slash(description='ᕕ( ᐛ )ᕗ', guild_ids=guild_ids)
    async def ping(self, ctx: SlashContext):
        embed = discord.Embed(title='Baby seals! ( ￫ᴥ￩ )', description=f' delay: {round(self.bot.latency * 1000)}ms')
        await respond(ctx, embed=embed)

    @cog_ext.cog_slash(description='(ﾟ Дﾟ ;)', guild_ids=guild_ids)
    async def huh(self, ctx: SlashContext):
        await respond(ctx, 'Baby seals! https://slushyseals.tumblr.com/post/187863187506/ᴥ-seal-text-emojis')

    @cog_ext.cog_slash(name='hi-danii', description='do this if you\'re danii', guild_ids=guild_ids)
    async def _hi_danii(self, ctx: SlashContext):
        await respond(ctx, 'https://http.cat/400')


def setup(bot):
    bot.add_cog(Test(bot))
