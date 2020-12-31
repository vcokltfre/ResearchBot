import discord
from discord.ext import commands

from bot.bot import Bot
from config.config import command_roles


def check(member: discord.Member, allowed_roles: list):
    roles = [role.name for role in member.roles]
    for role in roles:
        if role in allowed_roles:
            return True
    return False


class Pin(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, requests_R):
        if (reaction := str(requests_R.emoji.name)) not in ['📌', '🔙']:
            return
        if requests_R.user_id == self.bot.user.id or not check(
                (usr := self.bot.get_guild(requests_R.guild_id).get_member(requests_R.user_id)),
                command_roles.lvl2roles):
            return
        channel = self.bot.get_channel(requests_R.channel_id)
        message = await channel.fetch_message(requests_R.message_id)
        if reaction == '📌':
            await message.pin(reason=f"pinned by {usr.name}#{usr.discriminator}")
        elif reaction == '🔙':
            await message.unpin(reason=f"unpinned by {usr.name}#{usr.discriminator}")
        await message.remove_reaction(reaction, usr)


def setup(bot: Bot):
    bot.add_cog(Pin(bot))
