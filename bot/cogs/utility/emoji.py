import re
import discord
from discord.ext import commands

from bot.bot import Bot


class Emoji(commands.Cog):
    """Stop that pesky emoji spam"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.emoji = re.compile(r"<:.{2,32}:[0-9]{17,19}>")
        self.exempt = ["Administrator"]

    def is_exempt(self, member: discord.Member):
        roles = [role.name for role in member.roles]
        for role in roles:
            if role in self.exempt:
                return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.is_exempt(message.author):
            return
        if len(self.emoji.findall(message.content)) > 16:
            await message.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.is_exempt(after.author):
            return
        if len(self.emoji.findall(after.content)) > 16:
            await after.delete()


def setup(bot: Bot):
    bot.add_cog(Emoji(bot))
