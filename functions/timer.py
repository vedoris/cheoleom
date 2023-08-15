import discord
from discord.ext import commands
from utils.commands import slash_command
from discord.commands import ApplicationContext, Option
from asyncio import sleep


class timer(commands.Cog):
    @commands.Cog.listener()
    async def on_message(message):
        if message.author.id == 218010938807287808:
            onemin_tuple = (':sparkles:', ':cloud_lightning:', ':thunder_cloud_rain:', ':cloud:')
            tenmin_tuple = (':boom:')
            guild = bot.get_guild(guildId)
            channel = guild.get_channel(message.reference.channel_id)
            usercommand = await channel.fetch_message(message.reference.message_id)
            if message.startswith(onemin_tuple):
                sleep(60)
                await channel.send(f'<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.')
            elif message.startswith(tenmin_tuple):
                sleep(600)
                await channel.send(f'<@{usercommand.author.id}>님, 강화 쿨타임이 지났습니다.')
            else:
                pass
                

def setup(bot):
    bot.add_cog(timer())
