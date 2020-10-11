import discord
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import is_dev
from config.config import guild


class Status(commands.Cog):
    """A cog for automatically updating the bot's presence"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None
        
        if bot.cfg.has_attr("status_updates"):
            self.enabled = bot.cfg.get_attr("status_updates")
        else:
            self.enabled = True
            bot.cfg.set_attr("status_updates", True)
        self.enabled = False

    async def _set(self, status: str):
        await self.bot.change_presence(activity=discord.Game(name=status))

    async def _auto(self):
        if self.enabled:
            await self._set(f"with {self.guild.member_count} users")

    # Commands
    @commands.group(name="status", aliases=["presence"])
    @is_dev()
    async def status_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.channel.send("Usage: `!status <set | enable | disable> [new status]`")

    @status_group.command(name="set")
    async def status_set(self, ctx: commands.Context, *, status):
        await self._set(status)
        await ctx.send(f"Set status to `{status}`.")

    @status_group.command(name="enable")
    async def status_enable(self, ctx: commands.Context):
        self.enabled = True
        self.bot.cfg.set_attr("status_updates", True)
        await self._auto()
        await ctx.send("Enabled status updates.")

    @status_group.command(name="disable")
    async def status_disable(self, ctx: commands.Context):
        self.disabled = True
        self.bot.cfg.set_attr("status_updates", False)
        await ctx.send("Disabled status updates.")

    # Event listeners
    @commands.Cog.listener()
    async def on_ready(self):
        #self.guild = self.bot.get_guild(guild)
        #await self._auto()
        await self._set("MC@H community")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self._auto()

    @commands.Cog.listener()
    async def on_member_leave(self, member: discord.Member):
        await self._auto()


def setup(bot: Bot):
    bot.add_cog(Status(bot))
