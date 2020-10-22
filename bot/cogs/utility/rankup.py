import discord
from discord.ext import commands

from bot.bot import Bot


class Rankup(commands.Cog):

    def check_permission(self, author: discord.Member, allowed: list):
        roles = [role.name for role in author.roles]
        for role in roles:
            if role in allowed:
                return 0
        return 1

    async def rankup_user(self, user: discord.Member, role: str):
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))

    @commands.group(name='rankup')
    async def rankup(self, ctx: commands.Context):
        if not ctx.invoked_subcommand:
            return


    @rankup.command(name='Member', aliases=['M', 'm'])
    async def rankup_member(self, ctx: commands.Context, user: discord.Member):
        if self.check_permission(ctx.author, ['Administrator', 'Moderator', 'Staff',
                                              'Private Project Access', 'Private Chat Access']):
            return
        await self.rankup_user(user, 'Member')
        await ctx.send(f"{user.mention} has been given the Member role")

    @rankup.command(name='Project Contributor', aliases=['PC', 'pc'])
    async def rankup_pc(self, ctx: commands.Context, user: discord.Member):
        if self.check_permission(ctx.author, ['Administrator', 'Moderator', 'Staff',
                                              'Private Project Access']):
            return
        await self.rankup_user(user, 'Project Contributor')
        await ctx.send(f"{user.mention} has been given the Project Contributor role")

def setup(bot: Bot):
    bot.add_cog(Rankup(bot))