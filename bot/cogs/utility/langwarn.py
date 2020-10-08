# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
from googletrans import Translator, LANGUAGES

class Langwarn(commands.Cog):
    """Automagically tell people in their native language to speak english"""

    def __init__(self, bot):
        self.bot = bot
        self.t = Translator()
        self.b = {}
        self.m = "Hi, we've noticed you're speaking {0}, and while it's awesome you can speak another language, we'd appreciate it if you spoke english here for the benefit of out moderation team, thanks!"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user or len(message.content) < 12:
            return
        if any([role in [r.name for r in message.author.roles] for role in ["Administrator", "Moderator"]]): return
        if message.channel.id in [762748542787649586]: return
        lang = self.t.detect(message.content)
        if not lang.lang == "en":
            uid = str(message.author.id)
            if not uid in self.b:
                self.b[uid] = 1
            else:
                self.b[uid] += 1
            if self.b[uid] >= 3:
                text = self.t.translate(self.m.format(LANGUAGES[lang.lang.lower()]), dest=lang.lang)
                await message.channel.send(text.text)
                del self.b[uid]

def setup(bot):
    bot.add_cog(Langwarn(bot))
