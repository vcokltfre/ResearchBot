import discord
from discord.ext import commands

class PokeAboose(commands.Cog):
      def __init__(self, bot: commands.Bot):
          self.bot = bot
          self.vc1lovers = [280139294327308299]
      
      @commands.Cog.listener(name="on_voice_state_update")
      async def pokeaboose(self, poke: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
          if not poke.id in self.vc1lovers:
              return
          if after.channel == 720730080988627005:
              return await poke.edit(voice_channel=None)

def setup(bot: commands.Bot):
    bot.add_cog(PokeAboose(cog))
