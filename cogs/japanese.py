from discord.ext import commands
import requests


async def getJapaneseWordTranslation(ctx, word):
    url = "https://jisho.org/api/v1/search/words?keyword="
    response = requests.get(url + word)

    content = response.json()

    if content["meta"]["status"] != 200:
        return "Error: Could not communicate with API"

    print(content["data"][0]["jlpt"])

    output = "Kanji: " + (content["data"][0]["japanese"][0]["word"]) + "\t" \
             + "Hiragana: " + (content["data"][0]["japanese"][0]["reading"])

    return output


class Japanese(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, message):
        await ctx.send(await getJapaneseWordTranslation(ctx, message))


def setup(client):
    client.add_cog(Japanese(client))
