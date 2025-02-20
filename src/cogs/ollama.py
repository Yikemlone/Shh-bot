
import discord
from discord.ext import commands
from util.logger import logging, SHH_BOT

logger = logging.getLogger(SHH_BOT)

class Ollama(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.join_channel = "gamer"

async def setup(bot):
    await bot.add_cog(Ollama(bot))