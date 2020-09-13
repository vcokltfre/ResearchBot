import discord
from discord.ext import commands

from bot.bot import Bot


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
            message = await ctx.channel.send(msg)
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
        else:
            raise error


def setup(bot: Bot):
    bot.add_cog(fun(bot))
