import discord
import re
import json
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot
from bot.utils.config import ConfigUtil

AUDIT = 766321480421474322
audit_entry = re.compile(r"^`[0-9]+:`")
SUGGESTIONS = 774319616280232026
suggest_file = "./tmp/suggestions.json"


class Server(commands.Cog):
    """"""

    def __init__(self, bot: Bot):
        self.bot = bot

        self.sp = ConfigUtil(suggest_file, [])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.channel.id in [AUDIT, SUGGESTIONS]:
            return

        if message.author == self.bot.user or message.webhook_id:
            return

        if message.channel.id == AUDIT:
            if not audit_entry.match(message.content):
                await message.delete()
                await message.author.send("Invalid audit entry, entries should start with \"\\`NUM:\\`\"")
            return

        if message.channel.id == SUGGESTIONS:
            data = {
                "user":str(message.author),
                "content":message.content
            }
            ls = self.sp.read()
            ls.append(data)
            self.sp.data = ls
            self.sp.write()
            await message.channel.send("Your suggestion has been recorded and will be discussed in the next server meeting!", delete_after=15)


def setup(bot: Bot):
    bot.add_cog(Server(bot))
