import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot
from config.config import nick_request_channel_id as request_channel_id
from config.config import nick_accept_channel_id as accept_channel_id

command_timeout = 600
allowed_list = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;?@[\\]^_`{|}~ '


class Nickrequest(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="nick")
    # @commands.cooldown(1, command_timeout, commands.BucketType.user)
    async def nick(self, ctx: commands.Context, *, nick):
        acc_channel = self.bot.get_channel(accept_channel_id)
        nick = str(nick)
        nick.replace('"', '\"')
        nick.replace("'", "\'")

        # this looks if the request is valid
        for char in nick:
            if not char in allowed_list:
                await ctx.send(f'{ctx.author.mention}, please only use allowed characters', delete_after=5)
                await ctx.message.delete()
                return
        if not nick:
            await ctx.send(f'{ctx.author.mention}, please mention a nick to change to.', delete_after=5)
            await ctx.message.delete()
            return
        if ctx.channel.id != request_channel_id:
            await ctx.send(f'{ctx.author.mention}, please use the correct channel.', delete_after=5)
            await ctx.message.delete()
            return

        if len(nick) > 32:
            await ctx.send(f'{ctx.author.mention}, please mention a nick with 32 characters or less.', delete_after=5)
            await ctx.message.delete()
            return

        # this sends the embed to the selected channel
        embed = discord.Embed(title="Nickname Change Request", color=8359053)
        embed.add_field(name="Current Nick", value=f"{ctx.author.nick}")
        embed.add_field(name="Requested Nick", value=f"{nick}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Requester", value=f"{ctx.author.mention}")
        await ctx.message.add_reaction("✅")
        message = await acc_channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await asyncio.sleep(5)
        await ctx.message.delete()

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        # this rules out other reactions
        if payload.channel_id != accept_channel_id or payload.user_id == self.bot.user.id:
            return
        emoji = payload.emoji.name
        if emoji not in ['✅', '❌']:
            return

        # this get the channel, user, emoji and message
        channel = self.bot.get_channel(id=payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)

        server = self.bot.get_guild(msg.guild.id)

        easy_embed = msg.embeds[0].to_dict()
        user = server.get_member(int(easy_embed['fields'][2]['value'][3:-1]))
        reactor = server.get_member(int(payload.user_id))
        nickname = easy_embed['fields'][1]['value']

        if emoji == '✅':
            embed = discord.Embed(title="Nickname Change Request", color=3066993)
        elif emoji == '❌':
            embed = discord.Embed(title="Nickname Change Request", color=15158332)
        else:
            return

        embed.add_field(name="Current Nick", value=f"{user.nick}")
        embed.add_field(name="Requested Nick", value=f"{nickname}")
        embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
        embed.add_field(name="Requester", value=f"{user.mention}")

        # this applies the nickname or notifies the user of the denied request
        if emoji == '✅':
            embed.add_field(name="Accepted by", value=f"{reactor.mention}")
            await msg.edit(embed=embed)
            await msg.clear_reactions()
            await user.edit(nick=nickname)
        elif emoji == '❌':
            embed.add_field(name="Denied by", value=f"{reactor.mention}")
            await msg.edit(embed=embed)
            await msg.clear_reactions()
            await user.send(f"Your nickname change to {nickname}, was denied.")

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # this sends an error if the command is used too often
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            await ctx.send(msg, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            raise error


def setup(bot: Bot):
    bot.add_cog(Nickrequest(bot))
