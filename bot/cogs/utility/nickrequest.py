import discord
from discord.ext import commands
import asyncio
import string

from bot.bot import Bot
from config.config import nick_request_channel_id as request_channel_id
from config.config import nick_accept_channel_id as accept_channel_id

command_timeout = 600


class Nickrequest(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="nick")
    @commands.cooldown(1, command_timeout, commands.BucketType.user)
    async def nick(self, ctx: commands.Context, *, nick):
        acc_channel = self.bot.get_channel(accept_channel_id)
        nick = str(nick)

        # this looks if the request is valid
        nick = ''.join(allowed_character for allowed_character in nick if allowed_character in allowed_list)

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
        embed = discord.Embed(title="Nickname Change Request", color=0x00ff00)
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Current Nickname",value=f'{ctx.author.nick if ctx.author.nick else "Unassigned."}')
        embed.add_field(name="Requested Nickname",value=f'{nick}')
        embed.add_field(name="Requester",value=f"{ctx.author.mention}")
        embed.add_field(name="Message ID",value=f"{ctx.message.id}")
        embed.add_field(name="Channel ID",value=f"{ctx.channel.id}")
        this = await acc_channel.send(embed=embed)
        await this.add_reaction("✅")
        await this.add_reaction("❌")
        await ctx.message.add_reaction("✅")
        await asyncio.sleep(5)
        await ctx.message.delete()

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def there_reaction(self, requests_R):
        if requests_R.channel_id != accept_channel_id or requests_R.user_id == self.bot.user.id:
            return
        added_message = await self.bot.get_channel(request_channel_id).fetch_message(requests_R.message_id)
        reaction_ = str(requests_R.emoji.name)
        current_guild = self.bot.get_guild(requests_R.guild_id)
        
        if reaction_ not in ['✅','❌']:
            return
        
        easy_embed = added_message.embeds[0].to_dict()      
        if easy_embed['title'] == "Nickname Change Request":
            new_nick = easy_embed['fields'][1]['value']
            uuid = easy_embed['fields'][2]['value'][2:-1].replace('!','')
            user_ = current_guild.get_member(int(uuid))
            current_channel = current_guild.get_channel(int(easy_embed['fields'][4]['value']))
            original_message = await current_channel.fetch_message(int(easy_embed['fields'][3]['value']))
            if reaction_ == '✅':
                embed = discord.Embed(color=0x00ff00)
                embed.add_field(name="Previous Nickname",value=f'{user_.nick if user_.nick else "Unassigned."}')
                embed.add_field(name="Current Nickname",value=f'{new_nick}')
                embed.add_field(name="Fulfiller",value=f"{current_guild.get_member(requests_R.user_id).mention}",inline=False)
                await user_.edit(nick=new_nick)
                await original_message.add_reaction('✅')
            else:
                embed = discord.Embed(color=0xff0000)
                embed.add_field(name="Current Nickname",value=f'{user_.nick if user_.nick else "Unassigned."}')
                embed.add_field(name="Denied Nickname",value=f'{new_nick}')
                embed.add_field(name="Denier",value=f"{current_guild.get_member(requests_R.user_id).mention}",inline=False)
                await original_message.add_reaction('❌')
            embed.add_field(name="Requester",value=f"{user_.mention}")
            embed.add_field(name="Message ID",value=f"{easy_embed['fields'][3]['value']}")
            embed.add_field(name="Channel ID",value=f"{easy_embed['fields'][4]['value']}")
            embed.set_author(name=f"{user_.name}#{user_.discriminator}", icon_url=user_.avatar_url)    
            await added_message.clear_reactions()
            await added_message.edit(embed=embed)

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # this sends an error if the command is used too often
            msg = f'{ctx.author.mention}, this command is ratelimited, please try again in {error.retry_after}s.'
            await ctx.send(msg, delete_after=5)
            await asyncio.sleep(5)
            await ctx.message.delete()
        else:
            raise error


def setup(bot: Bot):
    bot.add_cog(Nickrequest(bot))
