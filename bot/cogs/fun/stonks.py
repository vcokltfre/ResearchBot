from yahoo_fin.stock_info import get_live_price
from discord.ext import commands
import asyncio

from bot.bot import Bot


class Stonks(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def getprice(stonk):
        return f"${round(get_live_price(stonk), 3)}"

    @commands.command(name="stonks")
    async def stonk_cmd(self, ctx, ticker='nvda'):
        pass#await ctx.send(f"Stonks for {ticker.upper()}: ${round(get_live_price(ticker), 3) if not ticker == 'vco' else 99999}")

    @commands.command(name="stonkwatch")
    async def stonkwatch(self, ctx, ticker='gme', interval: int = 5, reps: int = 500):
        if ctx.author.id != 297045071457681409:
            return await ctx.send("You don't have permission to use this command!")

        imsg = await ctx.send(f"{ticker.upper()}: {self.getprice(ticker)}")

        for i in range(reps):
            await asyncio.sleep(interval)
            await imsg.edit(content=f"[{str(i).zfill(4)}] {ticker.upper()}: {self.getprice(ticker)}")


def setup(bot: Bot):
    bot.add_cog(Stonks(bot))
