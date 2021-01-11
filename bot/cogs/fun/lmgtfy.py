import re
import random
from discord.ext import commands
from urllib.parse import quote_plus

from bot.bot import Bot
from config.config import command_roles

mention = re.compile(r"<@.?[0-9]*?>|@everyone|@here")


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
    async def lmgtfy(self, ctx: commands.Context, *, query):
        if mention.match(query):
            await ctx.send(f"{ctx.author.mention}{random.choice(self.insult)}")
            return
        await ctx.send(f"https://lmgtfy.app/?q={quote_plus(query)}")


def setup(bot: Bot):
    bot.add_cog(Lmgtfy(bot))
