import discord
from time import time
from discord.ext import commands

from bot.bot import Bot

ACH = 737298182912082072
WEEK = 24 * 3600 * 7

def deconstruct(snowflake: int):
    timestamp = (snowflake >> 22) + 1420070400000

    return timestamp // 1000


class Server(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        jt = deconstruct(member.id)
        dt = int(time()) - jt
        
        if dt < WEEK:
            ch = self.bot.get_channel(ACH)
            s = dt % 60
            m = (dt // 60) % 60
            h = (dt // 3600) % 24
            d = (dt // 86400) % 7
            await ch.send(f"NEW USER: {member.mention} ({member.id}) was created in the last week! ({d}d {h}h {m}m {s}s ago)")


def setup(bot: Bot):
    bot.add_cog(Server(bot))
