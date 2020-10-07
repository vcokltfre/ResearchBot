import discord
import string
from discord.ext import commands
from pathlib import Path

from bot.bot import Bot
from bot.utils.image import make_image, make_text


class Images(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.mentions = discord.AllowedMentions(everyone=False, users=False, roles=False)

        if not Path("./tmp/").exists():
            Path("./tmp/").mkdir()

    def check_name(self, filename):
        parts = filename.split(".")
        if len(parts) < 2:
            return False
        return parts.pop() in ["jpg", "bmp", "jpeg", "png"]

    @commands.group(name="image", aliases=["i", "im"])
    @commands.has_any_role("Administrator", "Moderator")
    async def img_grp(self, ctx: commands.Context):
        if ctx.invoked_subcommand == None:
            if len(ctx.message.attachments) == 1:
                attach = ctx.message.attachments[0]
                if not self.check_name(attach.filename):
                    return
                data = await attach.read()

                with Path("./tmp/image.png").open('wb') as f:
                    f.write(data)

                await ctx.send(make_text("./tmp/image.png")[:1995])

    @img_grp.command(name="encode", aliases=["e", "ec"])
    async def img_enc(self, ctx: commands.Context, *, text):
        make_image(text, "./tmp/img_out.png")
        await ctx.send(file=discord.File("./tmp/img_out.png", filename="encoded.png"), allowed_mentions=self.mentions)


def setup(bot: Bot):
    bot.add_cog(Images(bot))
