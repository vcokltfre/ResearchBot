import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot
from config.config import nick_request_channel_id as request_channel_id
from config.config import nick_accept_channel_id as accept_channel_id

reaction_timeout = 300
command_timeout = 600


class Nickrequest(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="nick")
    @commands.cooldown(1, command_timeout, commands.BucketType.user)
    async def nick(self, ctx: commands.Context, *, nick: str):
        rq_channel = self.bot.get_channel(accept_channel_id)

        # this looks if the request is valid
        if not nick:
            await ctx.send(f'{ctx.author.mention}, please mention a nick to change to.',delete_after=5)
            await ctx.message.delete()
            return
        if ctx.channel.id != request_channel_id:
            await ctx.send(f'{ctx.author.mention}, please use the correct channel.',delete_after=5)
            await ctx.message.delete()
            return

        if len(nick) > 32:
            message = await ctx.send(f'{ctx.author.mention}, please mention a nick with 32 characters or less.',delete_after=5)
            await ctx.message.delete()
            return

        # this sends the embed to the selected channel
        embed = discord.Embed(title="Nickname Change Request",color=0x00ff00)
        embed.set_field(name="Current Nick",value=f"{ctx.author.nick}")
        embed.set_field(name="Requested Nick",value=f"{nick}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.set_field(name="Requester",value="{ctx.author.mention}")
        embed.set_footer(text=f"{ctx.author.id}")
        await ctx.message.add_reaction("✅")
        message = await rq_channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        # this rules out other reactions
        if payload.channel_id != accept_channel_id:
            return
        if payload.user_id == self.bot.user.id:
            return

        # this get the channel, user, emoji and message
        channel = self.bot.get_channel(id=payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji.name

        server = self.bot.get_guild(msg.guild.id)
        
        easy_embed = msg.embeds[0].to_dict()
        user = server.get_member(int(easy_embed['fields'][2]['value'][2:-1]))
        nickname = easy_embed['fields'][1]['value']
        

        # this applies the nickname or notifies the user of the denied request
        if emoji == '✅':
            await user.edit(nick=nickname)
            await asyncio.sleep(3)
            await msg.delete()
        elif emoji == '❌':
            await user.send(f"Your nickname change to {nickname}, was denied.")
            await asyncio.sleep(3)
            await msg.delete()

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # this sends an error if the command is used too often
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            message = await ctx.channel.send(msg)
            await asyncio.sleep(5)
            await ctx.message.delete()
            await message.delete()
        else:
            raise error


def setup(bot: Bot):
    bot.add_cog(Nickrequest(bot))
