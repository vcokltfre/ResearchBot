import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot

stickbug_immune = [244459328847872000, 297045071457681409]

class fun(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="stickbug")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def stickbug(self, ctx, user: discord.Member):
        if user.id in stickbug_immune and ctx.author.id not in stickbug_immune:
            await ctx.send(f"Ha you thought!\n"
                           f"https://stickb.ug/d/{ctx.author.id}")
        else:
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


def setup(bot: Bot):
    bot.add_cog(fun(bot))
