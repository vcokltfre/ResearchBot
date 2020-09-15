import discord
import string
from discord.ext import commands

from bot.bot import Bot

stickbug_immune = [244459328847872000, 297045071457681409]
rgb_people = [256251362260549632, 738981683516145785]


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

    def make_ascii(self, text: str):
        return ''.join([c for c in text if c in string.printable])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in rgb_people:
            if "rgb" in self.make_ascii(message.content.lower()):
                await message.channel.send("RGB makes your PC faster")


def setup(bot: Bot):
    bot.add_cog(fun(bot))
