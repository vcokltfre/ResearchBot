import discord
import string
from discord.ext import commands

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785]


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    def make_ascii(self, text: str):
        return ''.join([c for c in text if c in string.printable])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")


def setup(bot: Bot):
    bot.add_cog(fun(bot))
