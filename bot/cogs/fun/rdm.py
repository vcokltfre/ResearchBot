from datetime import time
import discord
import random
from discord.ext import commands

from bot.bot import Bot
from bot.utils.checks import is_dev
from bot.utils.config import ConfigUtil


class Random(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.cfg = ConfigUtil("./config/maze.json")

    @commands.group(name="rdm")
    @is_dev()
    async def rdm_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            await ctx.send("Invalid usage.")

    @rdm_group.command(name="add")
    async def rdm_add(self, ctx: commands.Context, name: str, chance: int, num: int, author: int, *, content: str):
        self.cfg.set_attr(name, {"c":chance,"d":content,"n":num,"a":author})

    @commands.Cog.listener()
    async def on_message(self, message):
        conf = self.cfg.read()
        for key in conf:
            data = conf[key]
            if message.author.id == data['a'] and random.randint(0,data['c']) == data['n']:
                await message.channel.send(data['d'])



def setup(bot: Bot):
    bot.add_cog(Random(bot))
