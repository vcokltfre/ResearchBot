import discord
import re
import random
from discord.ext import commands

from bot.bot import Bot
from config.config import command_roles


class Lmgtfy(commands.Cog):
    """A cog for the lazy ones, Pythagoras_314"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.insult = [
            " thinks they are smart.",
            ", you dumb shit stop it.",
            " wins the idiot award for today.",
            " thought they were clever."
        ]

    @commands.command(name='lmgtfy')
    @commands.has_any_role(*command_roles.lvl0roles)
    async def lmgtfy(self, ctx: commands.Context, *args):
        for arg in args:
            if re.match('<@.?[0-9]*?>', arg) or arg in ["@here", "@everyone"]:
                await ctx.send(f"{ctx.author.mention}{random.choice(self.insult)}")
                return
        await ctx.send(f"https://lmgtfy.app/?q={'+'.join(args)}")


def setup(bot: Bot):
    bot.add_cog(Lmgtfy(bot))
