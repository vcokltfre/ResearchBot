import discord
from discord.ext import commands

from bot.bot import Bot


class Lmgtfy(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='lmgtfy')
    @commands.has_any_role('Administrator', 'Moderator', 'Staff', 'Private Project Access', 'Private Chat Access', 'Patron', 'Server Booster', 'Member')
    async def lmgtfy(self, ctx: commands.Context, *args):
        await ctx.send(f"https://lmgtfy.app/?q={'+'.join(args)}")

def setup(bot: Bot):
    bot.add_cog(Lmgtfy(bot))
