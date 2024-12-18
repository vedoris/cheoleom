import discord
from discord.ext import commands
from discord.commands import ApplicationContext
import os
import logging
import utils.logging
from asyncio import sleep
import pickle

logger = logging.getLogger("main")

class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 218010938807287808:
            onemin_tuple = (
                ":sparkles:",
                ":cloud_lightning:",
                ":thunder_cloud_rain:",
                ":cloud:",
            )
            tenmin_tuple = ":boom:"
            channel = self.bot.get_guild(message.reference.guild_id).get_channel(
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

def setup(bot: commands.Bot):
    bot.add_cog(Timer(bot))
