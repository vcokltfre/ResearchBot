import time
import asyncio
import discord
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot

mess = """
__**Here you can propose new projects!**__

__**BEFORE YOU MAKE A SUGGESTION:**__
:book: **Check if it hasn't been suggested already.** Use Discord's search function, check <#755121689913983136>, pins or ask in <#738860957685776395> if unsure.
:mag_right: **Google it!** A lot of seeds/world downloads are already publicly known!
:thinking: **Consider if what you're suggesting has any significance** to the community, be it historical or technical.

__**HOW TO MAKE A GOOD SUGGESTION:**__
:white_check_mark: Explain properly what you mean and why should we be interested.
:white_check_mark: Try to include a link or an image (where it makes sense).

:x: ***Blatant duplicates and spam will get deleted without notice!** :wastebasket:
Otherwise you'll get notified in <#738860957685776395> if there are any problems.
Repeatedly making bad suggestions will get your access to this channel removed!*


:warning:   :rotating_light:   :warning:   :rotating_light:   :warning:
__Blatantly ignoring this message will get you **muted** for a day!__
:warning:   :rotating_light:   :warning:   :rotating_light:   :warning:
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
