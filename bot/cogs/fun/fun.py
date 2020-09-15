import discord
import asyncio
import aiohttp
import aiofiles
import string
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785]


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

        if not Path("./temp").exists():
            Path("./temp").mkdir()

    def make_ascii(self, text: str):
        return ''.join([c for c in text if c in string.printable])

    @commands.command(name="stickbug")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def stickbug(self, ctx, user: discord.Member):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://stickb.ug/d/{user.id}") as resp:
                    f = await aiofiles.open('./temp/sb.mp4', mode='wb')
                    await f.write(await resp.read())
                    await f.close()
            await ctx.send(file=discord.File("./temp/sb.mp4"))

    @stickbug.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # this sends an error if the command is used too often
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            raise error


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")


def setup(bot: Bot):
    bot.add_cog(fun(bot))
