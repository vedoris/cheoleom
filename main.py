import discord
import os
import dotenv
import logging
import utils.logging
from discord.ext import commands, tasks
import time
from asyncio import sleep
import pickle

dotenv.load_dotenv()
utils.logging.setup_logging()

bot = commands.Bot(command_prefix="/", help_command=None, intents=discord.Intents.all())
aiodb = None
logger = logging.getLogger("main")

bot.start_time = time.time()


@bot.event
async def on_ready():
    guild_count = len(bot.guilds)

    logger.info(f"Logged in as {bot.user.name}")
    logger.info(f"Be used in {guild_count} guilds.")

    bot.change_status.start()


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"버전 0.1.0 - {len(bot.guilds)}개의 서버에서 작동 중"),
        )


# Timer
@bot.event
async def on_message(message):
    if message.author.id == 218010938807287808:
        onemin_tuple = (
            ":sparkles:",
            ":cloud_lightning:",
            ":thunder_cloud_rain:",
            ":cloud:",
        )
        tenmin_tuple = ":boom:"
        channel = bot.get_guild(message.reference.guild_id).get_channel(
            message.reference.channel_id
        )
        usercommand = await channel.fetch_message(message.reference.message_id)
        if os.path.isfile(f"{usercommand.author.id}.pkl"):
            if message.content.startswith(onemin_tuple):
                logger.info("Message detected.")
                await sleep(60)
                await channel.send(f"<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.")
            elif message.content.startswith(tenmin_tuple):
                await sleep(600)
                await channel.send(f"<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.")
            else:
                pass

# register / delete ID - https://github.com/Whitetiger0423/CutePoint main.py e57b7af (lazy)
@bot.slash_command(description="유저 정보를 등록합니다.")
async def 등록(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl") == False:
        embed = discord.Embed(
            title="등록", description="봇의 서비스에 등록합니다. 동의하지 않을 경우 서비스 이용에 제한이 있을 수 있습니다."
        )
        embed.add_field(name="수집하는 정보", value="유저의 디스코드 id", inline=False)

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                UserData = 1
                if interaction.user.id == ctx.user.id:
                    with open(f"{interaction.user.id}.pkl", "wb") as f:
                        pickle.dump(UserData, f)
                    new_embed = discord.Embed(
                        title="등록 완료", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"<@!{interaction.user.id}>님, 등록을 완료하였습니다. 아이디는 {interaction.user.id}입니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    new_embed = discord.Embed(
                        title="등록 취소", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"등록이 취소되었습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)
        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록된 유저", description="")
        embed.add_field(
            name="", value="이미 등록되었습니다. `/탈퇴` 명령어를 통해 탈퇴할 수 있습니다.", inline=False
        )
        await ctx.respond(embed=embed)


@bot.slash_command(description="봇 서비스를 탈퇴합니다.")
async def 탈퇴(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        embed = discord.Embed(
            title="탈퇴", description="봇의 서비스를 탈퇴합니다. 탈퇴할 경우 모든 데이터가 파기되며, 복구하기 어렵습니다."
        )
        embed.add_field(
            name="파기하는 정보", value="유저의 디스코드 id, 서비스 이용 중 가챠 기록", inline=False
        )

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    os.remove(f"{interaction.user.id}.pkl")
                    new_embed = discord.Embed(
                        title="탈퇴 완료", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"<@!{interaction.user.id}>님, 탈퇴를 완료하였습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    new_embed = discord.Embed(
                        title="탈퇴 취소", description=""
                    )
                    new_embed.add_field(
                        name="", value=f"탈퇴가 취소되었습니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self, embed=new_embed)

        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록하지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입해주세요.", inline=False)
        await ctx.respond(embed=embed)


# Load Cogs

for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(os.getenv("BOT_TOKEN"))
