import discord
from yahoo_fin.stock_info import get_live_price
from discord.ext import commands

from bot.bot import Bot


class Stonks(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="stonks")
    async def stonk_cmd(self, ctx, ticker='nvda'):
        await ctx.send(f"Stonks for {ticker.upper()}: ${round(get_live_price(ticker), 3) if not ticker == 'vco' else 99999}")


def setup(bot: Bot):
    bot.add_cog(Stonks(bot))
