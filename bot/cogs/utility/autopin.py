import time
import asyncio
import discord
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot

mess = """
__**Here you can suggest anything we should do!**__

__**BUT!** There's a few things you should consider before suggesting something:__
:book: **Please check if it hasn't been suggested already.** Use the search function, or ask in #suggestion-discussion.
:mag_right: A lot of seeds are already publicly known! Please look stuff up on Google before you suggest it.
:thinking: Consider if what you're suggesting has any significance, be it historical or technical.
:x: Blatant duplicates and spam will get deleted without notice! Otherwise you'll get notified in #suggestion-discussion if there are any problems.
__Common suggestions include:__ All the panoramas (we'll work on them later), MC Trailer (#trailer-resources), Herobrine picture (#herobrine-resources) Yogscast seed (4090136037452000329), DanTDM's lab seed (5021019576385777538), and various MC renders.
For more info, check the pinned messages.
"""

channel = 738836486199181312


class Autopin(commands.Cog):
    """Keep a message pinned at the bottom of a channel"""

    def __init__(self, bot: Bot):
        self.bot = bot
        if not Path("./data").exists():
            Path("./data").mkdir()

        self.p = Path("./data/ap.txt")

        if not self.p.exists():
            with self.p.open('w') as f:
                self.mid = None
        else:
            with self.p.open() as f:
                self.mid = int(f.read())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.channel.id != channel:
            return

        if self.mid:
            m = await message.channel.fetch_message(self.mid)
            await m.delete()

        m = await message.channel.send(mess)
        
        with self.p.open('w') as f:
            f.write(str(m.id))
        self.mid = m.id
        await asyncio.sleep(4)
        await m.clear_reactions()


def setup(bot: Bot):
    bot.add_cog(Autopin(bot))
