import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option

basic_commands = (
    discord.Embed(
        title="처럼 도움말",
        description="처럼의 명령어에 대해서 소개합니다.",
        color=0xFFFFFF,
    )
    .add_field(name="", value="", inline=False)
    )
)


class help(commands.Cog):
    @slash_command(description="봇의 도움말을 전송합니다.")
    async def help(
        self,
        ctx: ApplicationContext
    ):
        await ctx.respond(embed=basic_commands)


def setup(bot):
    bot.add_cog(help())
