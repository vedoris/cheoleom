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

    change_status.start()


@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"버전 0.1.0 - {len(bot.guilds)}개의 서버에서 작동 중"),
        )


# Load Cogs

for filename in os.listdir("functions"):
    if filename.endswith(".py"):
        bot.load_extension(f"functions.{filename[:-3]}")


bot.run(os.getenv("BOT_TOKEN"))
