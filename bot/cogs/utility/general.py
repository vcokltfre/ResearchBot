import discord
import time
import requests
import json
import parsedatetime
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import is_dev
from config.config import name, dmhook

def ensure_length(text, desired: int, char = '0'):
    while len(text) < desired:
        text = char + text
    return text


class General(commands.Cog):
    """A general purpose cog for tasks such as cog loading"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.cal = parsedatetime.Calendar()

    @commands.group(name="cogs")
    @is_dev()
    async def cogs_group(self, ctx: commands.Context):
        """Perform actions such as reloading cogs"""
        if ctx.invoked_subcommand == None:
            await ctx.channel.send(f"Invalid usage.")

    @cogs_group.command(name="load")
    async def load_cogs(self, ctx: commands.Context, *cognames):
        """Load a set of cogs"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                self.bot.load_extension(cog)
                log += f"Successfully loaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to load cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog loading: failed to load {cog}: {e}")

        self.bot.logger.info(f"Loaded cog(s):\n{log}")
        await ctx.send(log)

    @cogs_group.command(name="reload")
    async def reload_cogs(self, ctx: commands.Context, *cognames):
        """Reload a set of cogs"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                self.bot.reload_extension(cog)
                log += f"Successfully reloaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to reload cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog reloading: failed to reload {cog}: {e}")

        self.bot.logger.info(f"Reloaded cog(s):\n{log}")
        await ctx.send(log)

    @cogs_group.command(name="unload")
    async def unload_cogs(self, ctx: commands.Context, *cognames):
        """Unload a set of cogs - you cannot unload utility.general"""
        log = ""
        for cog in cognames:
            cog = "bot.cogs." + cog
            try:
                if cog == "bot.cogs.utility.general":
                    raise Exception("You cannot unload this cog!")
                self.bot.unload_extension(cog)
                log += f"Successfully unloaded cog {cog}\n"
            except Exception as e:
                log += f"Failed to unload cog {cog}: {e}\n"
                self.bot.logger.error(f"Cog unloading: failed to unload {cog}: {e}")

        self.bot.logger.info(f"Unloaded cog(s):\n{log}")
        await ctx.send(log)

    @commands.command(name="restart", aliases=["reboot", "shutdown"])
    @is_dev()
    async def restart(self, ctx: commands.Context):
        """Make the bot logout"""
        await ctx.send("Restarting...")
        await self.bot.change_presence(status=discord.Status.invisible)
        self.bot.logger.info(f"Shutting down {name}")
        await self.bot.close()

    @commands.command(name="ping")
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def ping(self, ctx: commands.Context, p: int = 2):
        t_start = time.time()
        m = await ctx.channel.send("Testing RTT for message editing.")
        send = time.time() - t_start
        await m.edit(content="Testing Message Edit: Run 1...")
        rtt1 = time.time() - t_start - send
        await m.edit(content="Testing Message Edit: Run 2...")
        rtt2 = time.time() - t_start - (rtt1 + send)
        await m.edit(content="Testing Message Edit: Run 3...")
        rtt3 = time.time() - t_start - (rtt1 + rtt2 + send)
        ds = time.time()
        await m.delete()
        delete = time.time() - ds

        avg = (rtt1 + rtt2 + rtt3) / 3
        minimum = min(rtt1, rtt2, rtt3)*1000
        maximum = max(rtt1, rtt2, rtt3)*1000

        embed = discord.Embed(title="ResearchBot Ping", description=f"Websocket latency: {round(self.bot.latency*1000, p)}ms", colour=0x6AFF6A)
        embed.add_field(name="Message Send", value=f"{round(send*1000, p)}ms")
        embed.add_field(name="Message Delete", value=f"{round(delete*1000, p)}ms")
        embed.add_field(name="Edit RTT Avg/Min/Max/Diff", value=f"{round(avg*1000, p)}ms / {round(minimum, p)}ms / {round(maximum, p)}ms / {round(maximum - minimum, p)}ms", inline=False)
        embed.add_field(name="Edit RTT Run 1", value=f"{round(rtt1*1000, p)}ms")
        embed.add_field(name="Edit RTT Run 2", value=f"{round(rtt2*1000, p)}ms")
        embed.add_field(name="Edit RTT Run 3", value=f"{round(rtt3*1000, p)}ms")

        await ctx.send(embed=embed)

    #DM Logger + Responder
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild:
            return
        if message.channel == message.author.dm_channel:
            data = {
                "username":str(message.author),
                "content":f"({message.author.id}) {message.content[:1950].replace('@', '')}",
                "avatar_url":str(message.author.avatar_url)
            }
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(dmhook, data=json.dumps(data), headers=headers)

    @commands.command(name="dm")
    @commands.has_any_role("Administrator")
    async def dm_user(self, ctx, member: discord.Member, *, message):
        await member.send(message)

    @commands.command(name="mimic")
    @is_dev()
    async def mimic(self, ctx: commands.Context, member: discord.Member, *, text):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=str(member.name))
        await webhook.send(content=text, avatar_url=str(member.avatar_url))
        await webhook.delete()

    @commands.command(name="time")
    @is_dev()
    async def gtime(self, ctx: commands.Context, *, tm):
        t, tstat = self.cal.parse(tm)
        y = t.tm_year
        mo = ensure_length(str(t.tm_mon), 2)
        d = ensure_length(str(t.tm_mday), 2)
        h = ensure_length(str(t.tm_hour), 2)
        mi = ensure_length(str(t.tm_min), 2)
        sc = ensure_length(str(t.tm_sec), 2)
        await ctx.send(f"{y}:{mo}:{d}@{h}:{mi}:{sc}")


def setup(bot: Bot):
    bot.add_cog(General(bot))
