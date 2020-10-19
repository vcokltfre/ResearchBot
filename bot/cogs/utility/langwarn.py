# -*- coding: utf-8 -*-
import re

from discord.ext import commands
import discord
import random
import asyncio
from googletrans import Translator, LANGUAGES

class Langwarn(commands.Cog):
    """Automagically tell people in their native language to speak english"""

    def __init__(self, bot):
        self.bot = bot
        self.t = Translator()
        self.b = {}
        self.m = "Hi, we've noticed you're speaking {0}, and while it's awesome you can speak another language, we'd appreciate it if you spoke english here for the benefit of out moderation team, thanks!"
        self.emotes = re.compile(r"<:.{2,32}:[0-9]{17,19}>")
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        content_filter = self.emotes.sub('',message.content).strip()
        if any([message.author == self.bot.user, len(content_filter) < 12, any(role.name in ['Administrator','Moderator'] for role in message.author.roles), message.channel.id in [762748542787649586]]):
            return      
        
        lang = self.t.detect(content_filter)
        if not lang.lang == 'en':
            user_id = str(message.author.id)
            self.b[user_id] = 1 if user_id not in self.b else self.b[user_id] + 1
 
            if self.b[user_id] >= 3:
                text = self.t.translate(self.m.format(LANGUAGES[lang.lang.lower()]), dest=lang.lang)
                await message.channel.send(text.text, delete_after=20)
                del self.b[user_id]

    @commands.command(name="aaaaa")
    @commands.has_any_role("Administrator")
    async def aaaaa(self, ctx, *, text):
        async with ctx.channel.typing():
            for i in range(12):
                text = self.t.translate(text, dest=random.choice([key for key in LANGUAGES])).text
                await asyncio.sleep(0.5)
            text = self.t.translate(text, dest="en").text
            await ctx.send(text)

def setup(bot):
    bot.add_cog(Langwarn(bot))
