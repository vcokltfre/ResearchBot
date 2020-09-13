import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot

reaction_timeout = 300
command_timeout = 600
request_channel_id =
accept_channel_id =


def check(reaction, user):
    return user.id not in ['h'] and bool(str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')


class Nickrequest(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="nick")
    @commands.cooldown(1, command_timeout, commands.BucketType.user)
    async def nick_member(self, ctx: commands.Context, *, nick: str):
        channel = self.bot.get_channel(accept_channel_id)

        if ctx.channel.id != request_channel_id:
            message = await ctx.send(f'{ctx.author.mention}, please use the correct channel.')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
            return

        if not nick:
            await ctx.send(f'{ctx.author.mention}, please mention a nick to change to.')
            return
        if len(nick) > 32:
            await ctx.send(f'{ctx.author.mention}, please mention a nick with 32 characters or less.')
            return

        embed = discord.Embed(description=f"{ctx.author.name} wants their nickname to be changed to '{nick}'.",
                              color=0x00ff00)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.message.add_reaction("✅")
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await asyncio.sleep(1)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=reaction_timeout, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(description=f"{ctx.author.name}'s request has timed out.", color=0x0000ff)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('🕒')
        else:
            if str(reaction) == '✅':
                embed = discord.Embed(description=f"{ctx.author.name}'s nickname has been modified to {nick}",
                                      color=0xff0000)
                await ctx.author.edit(nick=nick)
            elif str(reaction) == '❌':
                embed = discord.Embed(description=f"{ctx.author.name}'s request has been denied.", color=0xff0000)
                await ctx.message.clear_reactions()
                await ctx.message.add_reaction('❌')
            embed.set_footer(text=f"{user.name}#{user.discriminator} approved")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await message.clear_reactions()
        await message.edit(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Nickrequest(bot))
