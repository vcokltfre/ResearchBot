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
    async def nick(self, ctx: commands.Context, *, nick):
        channel = self.bot.get_channel(accept_channel_id)
        # this looks if the request is valid

        if not nick:
            message = await ctx.send(f'{ctx.author.mention}, please mention a nick to change to.')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
            return

        nick = str(nick)

        if ctx.channel.id != request_channel_id:
            message = await ctx.send(f'{ctx.author.mention}, please use the correct channel.')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
            return

        if len(nick) > 32:
            message = await ctx.send(f'{ctx.author.mention}, please mention a nick with 32 characters or less.')
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
            return

        # this sends the embed to the selected channel
        embed = discord.Embed(description=f"{ctx.author.name} wants their nickname to be changed to '{nick}'.",
                              color=0x00ff00)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.id}")
        await ctx.message.add_reaction("✅")
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != accept_channel_id:
            return
        if payload.user_id == self.bot.user.id:
            return

        channel = self.bot.get_channel(id=payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji.name
        server = self.bot.get_guild(msg.guild.id)
        user = server.get_member(int(msg.embeds[0].footer.text))
        nickname = msg.embeds[0].description
        nickname = nickname.replace(f"{user.name} wants their nickname to be changed to '", "")
        nickname = nickname.replace("'.", "")

        if emoji == '✅':
            await user.edit(nick=nickname)
            await asyncio.sleep(3)
            await msg.delete()
        elif emoji == '❌':
            await user.send("Your nickname change request was denied.")
            await asyncio.sleep(3)
            await msg.delete()

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            message = await ctx.channel.send(msg)
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
        else:
            raise error


def setup(bot: Bot):
    bot.add_cog(Nickrequest(bot))
