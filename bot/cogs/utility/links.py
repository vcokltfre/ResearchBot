import pyourls3
import whois
import discord
import re
from discord.ext import commands

from bot.bot import Bot
from config.config import yourlspw


class Links(commands.Cog):
    """A cog for shortening links"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.yourls = pyourls3.Yourls(addr='https://mcatho.me/yourls-api.php', user='bot', passwd=yourlspw)

    async def check(self, message):
        if any(role_check in ['Moderator','Administrator'] for role_check in [role.name for role in message.author.roles]):
            return
        
        if self.bot.user == message.author:
            return
        words = ["discord.gg/", "com/invite/", "discord.io"]

        for word in words:
            if word in message.content:
                return await message.delete()

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def shorturl(self, ctx, url, short=None):
        """ creates a short mcatho.me url """
        try:
            if (short == None):
                surl = self.yourls.shorten(url)
            else:
                if url.startswith("https://mcatho.me") or url.startswith("http://mcatho.me") or url.startswith("mcatho.me"):
                    await ctx.send("I refuse to do that because you are stupid!")
                    return
                else:
                    surl = self.yourls.shorten(url, keyword=short)
            await ctx.send("URL got shortened:\nLong URL:```"+surl['url']['url']+"```Short URL:```"+surl['shorturl']+"```")
        except:
            await ctx.send("The keyword probably already exists! `"+short+"`", delete_after=10)

    @commands.command()
    @commands.has_any_role("Administrator", "Moderator", "Big Brain")
    async def urlstats(self, ctx, url=None):
        """ Get Stats from shortend URL's """
        if url == None:
            await ctx.send("!urlstats <keyword/shorturl | all>")
            return
        if url == "all":
            urls = self.yourls.stats()
            await ctx.send("General link statistics:\nTotal Links: ```"+urls['total_links']+"```Total Clicks:```"+urls['total_clicks']+"```")
        else:
            try:
                urls = self.yourls.url_stats(url)
                await ctx.send("Stats for shortened URL:```"+urls['shorturl']+"```Long URL:```"+urls['url']+"```Clicks:```"+urls['clicks']+"```Created:```"+urls['timestamp']+"```")
            except:
                await ctx.send("The keyword/shorturl probably doesn't exist! `"+url+"`", delete_after=10)

    @commands.command(name="whois")
    @commands.has_any_role("Administrator", "Moderator")
    async def whois_lookup(self, ctx: commands.Context, domain: str):
        domain = whois.query(domain)

        expiry = f"{domain.expiration_date.year}/{domain.expiration_date.month}/{domain.expiration_date.day}"
        creation = f"{domain.creation_date.year}/{domain.creation_date.month}/{domain.creation_date.day}"
        registrar = domain.registrar
        name = domain.name

        msg = f"WHOIS lookup for {name}:\nRegistrar: {registrar}\nCreation date: {creation}\nExpiry date: {expiry}\n"
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.check(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.check(after)


def setup(bot: Bot):
    bot.add_cog(Links(bot))
