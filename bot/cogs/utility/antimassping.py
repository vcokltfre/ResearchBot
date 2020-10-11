import discord
from discord.ext import commands

class AntiMassPing(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.max_mentions = 6

    @commands.Cog.listener(name="on_message")
    async def mess(self,message_object):
        if any(role_check in ['Big Brain','Moderator','Administrator'] for role_check in [role.name for role in message_object.author.roles]):
            return
        matches = set(message_object.mentions)
        if len(matches) < self.max_mentions:
            return
        muted_role = discord.utils.get(message_object.guild.roles, name="Muted")
        await message_object.author.add_roles(muted_role)
        embed = discord.Embed(title="Mass Ping",description=f"AntiSpam has detected a mass ping from the user {message_object.author.mention}.",color=0xff0000)
        mention_values = ', '.join(elem.mention for elem in matches)
        if len(mention_values) > 1024:
            embed.add_field(name="1 - Pinged Users:",value=mention_values[:mention_values[:1024].rfind('>')+1])
            embed.add_field(name="2 - Pinged Users:",value=mention_values[mention_values[:1024].rfind('>')+3:])
        else:
            embed.add_field(name="Pinged Users:",value=mention_values)
        embed.set_author(name=f"{message_object.author.name}#{message_object.author.discriminator}", icon_url=message_object.author.avatar_url)
        embed.set_footer(text="Mass pinging is not tolerated in this server. The associated user has been indefinitely muted.")
        this = await message_object.channel.send(embed=embed)
        await this.pin()

def setup(bot):
    bot.add_cog(AntiMassPing(bot))
