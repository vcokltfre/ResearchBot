import discord
from discord.ext import commands

from bot.bot import Bot


class Automod(commands.Cog):
    """Auto moderator"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def check(self, message):
        if any(role_check in ['Administrator'] for role_check in [role.name for role in message.author.roles]):
            return
        if self.bot.user == message.author:
            return

        words = ["learn-js", "learnjs"]

        for word in words:
            if word in message.content:
                return await message.delete()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.check(after)


def setup(bot: Bot):
    bot.add_cog(Automod(bot))
