import discord
import string
import random
from pathlib import Path
from discord.ext import commands
from discord.utils import get

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785, 149322096814718987]
ignore = [738029979899789315]


class Fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel = None

        try:
            with Path("/home/vcokltfre/quotes.txt").open() as f:
                self.quotes = [l for l in f.readlines()]
        except:
            self.bot.logger.warn("Failed to load quotes")

    def make_ascii(self, text: str):
        return ''.join([c for c in text if c in string.ascii_letters])

    @commands.command(name="do")
    async def doyouloveme(self, ctx, *, content):
        if not content == "you love me?":
            return
        if not ctx.author.id in [297045071457681409, 243233669148442624, 298190347614552066]:
            return await ctx.send(f"No, I dont love you {ctx.author.mention}")
        await ctx.send("Of course I still love you")

    @commands.command(name="quote")
    async def quote(self, ctx):
        await ctx.send(random.choice(self.quotes))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.category and message.channel.category.id in ignore:
            return
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")
        if random.randint(0,250) == 69:
            await message.reply("👀")
        #if random.randint(0,150) == 68:
        #    await message.add_reaction("🤪")
        if message.content == "@someone" and message.author.id == 297045071457681409:
            await message.channel.send(f"<@!{random.choice(message.guild.members).id}>")
        if "doors" in message.content and not random.randint(0, 5):
            await message.reply("doors")

    @commands.command(name="muteme")
    @commands.guild_only()
    async def mute_me(self, ctx):
        mr = get(ctx.guild.roles, name="Muted")
        await ctx.author.add_roles(mr)
        await ctx.send("Okie")


def setup(bot: Bot):
    bot.add_cog(Fun(bot))
