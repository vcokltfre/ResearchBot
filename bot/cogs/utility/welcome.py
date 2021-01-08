import discord
from discord.ext import commands

from config.config import welcome_channel


class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        c = self.bot.get_channel(welcome_channel)
        await c.send(f"Welcome {member.mention} to Minecraft@Home!", allowed_mentions=discord.AllowedMentions(users=False))


def setup(bot):
    bot.add_cog(Welcome(bot))
