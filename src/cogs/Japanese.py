import discord
from discord.ext import commands
import requests


class Japanese(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="translate", description="This will translate a word to Japanese.")
    @discord.app_commands.describe(message="The word you want to translate.")
    async def translate(self, interaction : discord.Interaction, message : str):
        await interaction.response.send_message(await self.getJapaneseWordTranslation(message))


    async def getJapaneseWordTranslation(self, message):
        url = "https://jisho.org/api/v1/search/words?keyword="
        response = requests.get(url + message)
        content = response.json()

        if content["meta"]["status"] != 200:
            return "Error: Could not communicate with API"

        output = "Kanji: " + (content["data"][0]["japanese"][0]["word"]) + "\t" \
                + "Hiragana: " + (content["data"][0]["japanese"][0]["reading"])

        return output


async def setup(bot):
    await bot.add_cog(Japanese(bot))
