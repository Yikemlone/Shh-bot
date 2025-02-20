import discord
from discord.ext import commands
from util.japaneseconnection import JapaneseConnection
from util.logger import logging, SHH_BOT

logger = logging.getLogger(SHH_BOT)


class Japanese(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="translate", description="This will translate a word to Japanese.")
    @discord.app_commands.describe(message="The word you want to translate.")
    async def translate(self, interaction : discord.Interaction, message : str):
        logger.info(f"Translaiting: {message}")
        translation = await JapaneseConnection.get_data(message)
        await interaction.response.send_message(translation)


async def setup(bot):
    await bot.add_cog(Japanese(bot))
