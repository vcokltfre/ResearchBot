import discord
import nbt
import requests
from pathlib import Path
from discord.ext import commands

from bot.bot import Bot


class SeedParse(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

        if not Path("./tmp").exists():
            Path("./tmp/").mkdir()

    @commands.group(name="mc")
    @commands.has_any_role("Private Chat Access", "Moderator", "Administrator", "Staff")
    async def mc_g(self, ctx: commands.Context):
        pass

    @mc_g.command(name="level")
    async def mc_level(self, ctx: commands.Context):
        if len(ctx.message.attachments) != 1:
            return await ctx.send("You must attach a level file.")

        file = ctx.message.attachments[0]

        if not file.filename.endswith(".dat"):
            return await ctx.send("File must be a dat file.")

        content = requests.get(file.url).content

        with Path("./tmp/level.dat").open('wb') as f:
            f.write(content)

        file = nbt.nbt.NBTFile("./tmp/level.dat", 'rb')
        try:
            await ctx.send(f"The seed is {file['Data']['RandomSeed'].value}")
        except:
            await ctx.send(f"The seed is {file['Data']['WorldGenSettings']['seed'].value}")


def setup(bot: Bot):
    bot.add_cog(SeedParse(bot))
