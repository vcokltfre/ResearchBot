import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from bot.bot import Bot
from bot.utils.config import ConfigUtil


class Status(commands.Cog):
    """A cog for showing the terms and guidelines"""

    def __init__(self, bot: Bot):
        self.bot = bot
        toscfg = ConfigUtil("./static/tos.json")
        tos = toscfg.get_attr("tos")
        dgl = toscfg.get_attr("dgl")

        tmp = []
        for item in tos:
            for name in item['names']:
                tmp.append((name, f"You may not use Discord to {item['content']}"))
        for item in dgl:
            for name in item['names']:
                tmp.append((name, item['content']))
        self.entries = dict(tmp)

    @commands.command(name="tos", aliases=["dgl", "terms", "guidelines"])
    @commands.cooldown(1, 10, BucketType.channel)
    async def tos(self, ctx, entry):
        if not entry in self.entries:
            await ctx.send("That item wasn't a valid entry.", delete_after=10)
            return


        content = self.entries[entry]
        await ctx.send(f"> {content}")

def setup(bot: Bot):
    bot.add_cog(Status(bot))
