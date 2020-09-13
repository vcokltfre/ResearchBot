import discord
from discord.ext import commands

from bot.bot import Bot


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="stickbug")
    async def stickbug(self, ctx, user: discord.Member):
        await ctx.send(f"https://stickb.ug/d/{user.id}")


def setup(bot: Bot):
    bot.add_cog(fun(bot))
