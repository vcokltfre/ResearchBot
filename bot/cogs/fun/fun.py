import discord
from discord.ext import commands

from bot.bot import Bot


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None


def setup(bot: Bot):
    bot.add_cog(fun(bot))
