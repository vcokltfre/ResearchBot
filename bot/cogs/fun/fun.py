import discord
import string
from discord.ext import commands

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785]
h_channel = 756100804892557372


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel = None

    def make_ascii(self, text: str):
        return ''.join([c for c in text if c in string.printable])

    @commands.command(name="do")
    async def doyouloveme(self, ctx, *, content):
        if not content == "you love me?":
            return
        if not ctx.author.id in [297045071457681409]:
            return await ctx.send("No, I dont")
        await ctx.send("Of course I still love you")

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(h_channel)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")
        if message.channel.id == h_channel and not message.content == 'h':
            await message.delete()
        if message.channel.id == h_channel and len(message.attachments) != 0:
            await message.delete()

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
    bot.add_cog(fun(bot))
