import discord
from discord.ext import commands

from bot.bot import Bot
from config.config import command_roles


class Lmgtfy(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='lmgtfy')
    @commands.has_any_role(*command_roles.lvl0roles)
    async def lmgtfy(self, ctx: commands.Context, *args):
        await ctx.send(f"https://lmgtfy.app/?q={'+'.join(args)}")

def setup(bot: Bot):
    bot.add_cog(Lmgtfy(bot))
