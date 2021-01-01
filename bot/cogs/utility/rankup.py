import discord
from discord.ext import commands
from typing import Optional

from bot.bot import Bot
from config.config import command_roles


class Rankup(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def rankup_user(self, ctx, user: discord.Member, role: str):
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await ctx.send(f"{user.mention} has been given the {role} role")

    def check(self, member: discord.Member, rolz: list):
        roles = [role.name for role in member.roles]
        for role in roles:
            if role in rolz:
                return True
        return False

    @commands.group(name="rankup")
    @commands.has_any_role(*command_roles.lvl1roles)
    async def rankup(self, ctx: commands.Context, *, user: Optional[discord.Member]):
        if not ctx.invoked_subcommand and user:
            if not self.check(ctx.author, command_roles.lvl2roles):
                return await self.rankup_member(ctx, user)
            return await self.auto(ctx, user)

    @rankup.command(name="Member", aliases=["M", "m", "member"])
    async def rankup_member(self, ctx, user: discord.Member):
        await self.rankup_user(ctx, user, 'Member')

    @rankup.command(name="Project Contributor", aliases=["PC", "pc"])
    @commands.has_any_role(*command_roles.lvl2roles)
    async def rankup_pc(self, ctx, user: discord.Member):
        await self.rankup_user(ctx, user, 'Project Contributor')

    @rankup.command(name="auto")
    async def auto(self, ctx, user: discord.Member):
        msg = await ctx.send(f"Select the role you want to give {user.mention}\n"
                             f"Select 1️⃣ for Member\nSelect 2️⃣ for Project Contributor")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")

        def check(reaction, author):
            return author == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣"]

        try:
            reaction, author = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await msg.edit(content="Member rankup menu timed out.")
            return

        if str(reaction.emoji) == "1️⃣":
            await self.rankup_user(ctx, user, 'Member')
            await msg.delete()
        elif str(reaction.emoji) == "2️⃣":
            await self.rankup_user(ctx, user, 'Project Contributor')
            await msg.delete()

        else:
            await self.rankup_user(ctx, user, 'Member')


def setup(bot: Bot):
    bot.add_cog(Rankup(bot))
