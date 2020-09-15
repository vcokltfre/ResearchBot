import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot

rgb_people = [256251362260549632, 738981683516145785]


class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="stickbug")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def stickbug(self, ctx, user: discord.Member):
        await ctx.send(f"https://stickb.ug/d/{user.id}")
        
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
            if "rgb" in message.content.lower():
                await message.channel.send("RGB makes your PC faster")


def setup(bot: Bot):
    bot.add_cog(fun(bot))
