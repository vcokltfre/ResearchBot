import discord
from discord.ext import commands

from bot.bot import Bot

allowed_list = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;?@[\\]^_`{|}~ '
max_nick_size = 32


class Wiki(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command("wikiname")
    @commands.has_role("Wiki Editor")
    async def wikiname(self, ctx: commands.Context, name: str):
        author: discord.Member = ctx.author

        new_nick = author.display_name + f" [{name} on WIKI]"
        if len(new_nick) > max_nick_size:
            return await ctx.send("Name too long! Make a nickname request instead with a shorter total name!")
        await author.edit(nick=new_nick, reason="WIKI name")


def setup(bot: Bot):
    bot.add_cog(Wiki(bot))
