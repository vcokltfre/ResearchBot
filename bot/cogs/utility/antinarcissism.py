"""
7x @ 2020-10-13
"""

import discord
from discord.ext import commands

class AntiNarcissism(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    async def cog_command_error(self, ctx, error):
        return await ctx.send(f"Error @ Cog.AntiNarcissism: `{error.original}`")
        
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def narcissism_check(self,payload: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id) 
        
        if any(role.name in ['Administrator','Moderator'] for role in message.author.roles):
            return
            
        if message.author.id != payload.user_id:
            return

        await message.remove_reaction(payload.emoji, message.author)
        
def setup(bot: commands.Bot):
    bot.add_cog(AntiNarcissism(bot))
