import discord
import os
import dotenv
import logging
import utils.logging
from discord.ext import commands
import time
from asyncio import sleep

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

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"버전 0.0.0 - {guild_count}개의 서버에서 작동 중"),
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
        if message.content.startswith(onemin_tuple):
            logger.info("Message detected.")
            await sleep(60)
            await channel.send(f"<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.")
        elif message.content.startswith(tenmin_tuple):
            await sleep(600)
            await channel.send(f"<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.")
        else:
            pass


# Load Cogs

for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(os.getenv("BOT_TOKEN"))
