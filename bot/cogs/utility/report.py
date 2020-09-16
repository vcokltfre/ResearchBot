import discord
from discord.ext import commands
import asyncio

from bot.bot import Bot
from config.config import token, name, log_level, log_type
from config.config import report_channel_id as report_channel_id
from config.config import report_lvls_amount
from config.config import report_accept_channel_ids as accept_channel_ids


class TooFewArguments(Exception):
    pass


class Report(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild = None

    @commands.command(name="report")
    async def report(self, ctx: commands.Context, lvl: int, reported_msg: discord.Message):
        acc_channels = []
        for channel in accept_channel_ids:
            acc_channels.append(self.bot.get_channel(channel))

        rep_lvls = report_lvls_amount + 1

        # this looks if the request is valid
        if lvl not in range(1, rep_lvls):
            await ctx.send(f'{ctx.author.mention}, please only use levels 1-{report_lvls_amount}.', delete_after=5)
            await ctx.message.delete()
            return
        if ctx.channel.id != report_channel_id:
            await ctx.send(f'{ctx.author.mention}, please use the correct channel.', delete_after=5)
            await ctx.message.delete()
            return

        lvl = lvl - 1

        # this sends the embed to the selected channel
        embed = discord.Embed(title="Reported Message:", color=15158332)
        embed.add_field(name="Reported Message Author", value=f"{reported_msg.author.mention}")
        if len(reported_msg.content) < 1024:
            embed.add_field(name="Reported Message Content", value=f"{reported_msg.content}")
        else:
            embed.add_field(name="Reported Message Content (1)", value=f"{reported_msg.content[:1024]}")
            embed.add_field(name="Reported Message Content (2)", value=f"{reported_msg.content[1024:]}")
        embed.add_field(name="Reported by:", value=f"{ctx.author.mention}")
        embed.add_field(name="Link to message:", value=f"{reported_msg.jump_url}")
        await ctx.message.add_reaction("✅")
        message = await acc_channels[lvl].send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await asyncio.sleep(5)
        await ctx.message.delete()

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        # this rules out other reactions
        if payload.channel_id not in accept_channel_ids or payload.user_id == self.bot.user.id:
            return
        emoji = payload.emoji.name
        if emoji not in ['✅', '❌']:
            return

        channel = self.bot.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        easy_embed = msg.embeds[0].to_dict()

        server = self.bot.get_guild(msg.guild.id)
        reactor = server.get_member(int(payload.user_id))

        field_reported_msg_author = easy_embed['fields'][0]['value']
        if easy_embed['fields'][1]['name'] == "Reported Message Content":
            field_reported_msg_content = easy_embed['fields'][1]['value']
        else:
            field_reported_msg_content_1 = easy_embed['fields'][1]['value']
            field_reported_msg_content_2 = easy_embed['fields'][2]['value']
        field_reporter = easy_embed['fields'][-2]['value']
        field_url = easy_embed['fields'][-1]['value']
        channel_id = field_url.split('/')[-2]
        message_id = field_url.split('/')[-1]

        rp_channel = server.get_channel(int(channel_id))
        try:
            rp_message = await rp_channel.fetch_message(int(message_id))
        except discord.NotFound:
            embed = discord.Embed(title="Reported Message:", color=15105570)
            embed.set_author(name="Warning: Message couldn't be found")
            embed.add_field(name="Reported Message Author", value=f"{field_reported_msg_author}")
            if easy_embed['fields'][1]['name'] == "Reported Message Content":
                embed.add_field(name="Reported Message Content", value=f"{field_reported_msg_content}")
            else:
                embed.add_field(name="Reported Message Content (1)", value=f"{field_reported_msg_content_1}")
                embed.add_field(name="Reported Message Content (2)", value=f"{field_reported_msg_content_2}")
            embed.add_field(name="Reported by:", value=f"{field_reporter}")
            embed.add_field(name="Link to message:", value=f"{field_url}")
            await msg.edit(embed=embed)
            await msg.clear_reactions()
            return

        embed = discord.Embed(title="Reported Message:", color=3066993)
        embed.add_field(name="Reported Message Author", value=f"{field_reported_msg_author}")
        if easy_embed['fields'][1]['name'] == "Reported Message Content":
            embed.add_field(name="Reported Message Content", value=f"{field_reported_msg_content}")
        else:
            embed.add_field(name="Reported Message Content (1)", value=f"{field_reported_msg_content_1}")
            embed.add_field(name="Reported Message Content (2)", value=f"{field_reported_msg_content_2}")
        embed.add_field(name="Reported by:", value=f"{field_reporter}")
        embed.add_field(name="Link to message:", value=f"{field_url}")

        if emoji == '✅':
            embed.add_field(name="Message deletion approved by:", value=f"{reactor.mention}")
            embed.set_author(name="Message was deleted!")
            await msg.edit(embed=embed)
            await msg.clear_reactions()
            await rp_message.delete()
        elif emoji == '❌':
            embed.add_field(name="Message deletion denied by:", value=f"{reactor.mention}")
            await msg.edit(embed=embed)
            await msg.clear_reactions()

    @report.error
    async def report_error(self, ctx, error):
        # this sends a message if the command is not properly used
        if isinstance(error, (commands.errors.BadArgument, commands.errors.MissingRequiredArgument)):
            msg = f'{ctx.author.mention}, this command is used like this:\n' \
                  f'!report report_level[1-{report_lvls_amount}] message_url'
            await ctx.send(msg, delete_after=5)
            await ctx.message.delete()
        else:
            raise error


def setup(bot: Bot):
    if len(accept_channel_ids) < report_lvls_amount:
        raise TooFewArguments("You are missing one or more channel ids in the config!")
    bot.add_cog(Report(bot))
