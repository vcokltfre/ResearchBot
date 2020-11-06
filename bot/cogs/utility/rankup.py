import discord
from discord.ext import commands

from bot.bot import Bot


class Rankup(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def rankup_user(self, ctx, user: discord.Member, role: str):
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await ctx.send(f"{user.mention} has been given the {role} role")

    @commands.command(name='rankup')
    @commands.has_any_role('Administrator', 'Moderator', 'Staff', 'Private Project Access', 'Private Chat Access')
    async def rankup(self, ctx: commands.Context, *args):
        usr = await commands.MemberConverter().convert(ctx, args[-1])

        if args[0] in ['Member', 'M', 'm']:
            await self.rankup_user(ctx, usr, 'Member')

        elif args[0] in ['Project Contributor', 'PC', 'pc'] \
                and commands.has_any_role('Administrator', 'Moderator', 'Staff', 'Private Project Access'):
            await self.rankup_user(ctx, usr, 'Member')

        elif commands.has_any_role('Administrator', 'Moderator', 'Staff', 'Private Project Access'):
            msg = await ctx.send(f"Select the role you want to give {usr.mention}\n"
                                 f"Select 1️⃣ for Member\nSelect 2️⃣ for Project Contributor")
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣"]

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except:
                await msg.edit(content="Member rankup menu timed out.")
                return

            if str(reaction.emoji) == "1️⃣":
                await self.rankup_user(ctx, usr, 'Member')
                await msg.delete()
            elif str(reaction.emoji) == "2️⃣":
                await self.rankup_user(ctx, usr, 'Project Contributor')
                await msg.delete()

        else:
            await self.rankup_user(ctx, usr, 'Member')


def setup(bot: Bot):
    bot.add_cog(Rankup(bot))
