import discord
import string
import random
from pathlib import Path
from discord.ext import commands

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785, 149322096814718987]
h_channel = 756100804892557372


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
        if not ctx.author.id in [297045071457681409]:
            return await ctx.send(f"No, I dont love you {ctx.author.mention}")
        await ctx.send("Of course I still love you")

    @commands.command(name="quote")
    async def quote(self, ctx):
        await ctx.send(random.choice(self.quotes))

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(h_channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")
        if random.randint(0,100) == 69:
            await message.add_reaction("👀")
        if message.content == "@someone" and message.author.id == 297045071457681409:
            await message.channel.send(f"<@!{random.choice(message.guild.members).id}>")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.channel.id == h_channel:
            await after.delete()

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.channel_id == h_channel:
            mess = await self.channel.fetch_message(payload.message_id)
            await mess.delete()


def setup(bot: Bot):
    bot.add_cog(Fun(bot))
