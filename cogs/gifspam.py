import os
import urllib
import requests
from urllib import parse
from discord.ext import commands
from dotenv import load_dotenv


class GifSpam(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.gifOn = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ctx = await self.client.get_context(message)

        # await self.japanese(ctx, message.content.lower())

        if self.gifOn:
            await self.postGif(message)

    @commands.command()
    async def gif(self, ctx):
        if self.gifOn:
            self.gifOn = False
        else:
            self.gifOn = True

    async def postGif(self, message):
        load_dotenv(".env")

        ctx = await self.client.get_context(message)
        word = message.content

        url = "http://api.giphy.com/v1/gifs/search?"

        params = urllib.parse.urlencode({
            "q": f"{word}",
            "api_key": os.getenv("GIF_API_KEY"),
            "limit": "1"
        })

        response = (requests.get(url + params))

        # Returns Dict type
        gif = response.json()

        # List type of length 1
        gifData = gif["data"]

        # Dict inside of the list
        if len(gifData) == 0:
            return

        gifDataDict = gifData[0]

        await ctx.send(gifDataDict["url"])

    async def japanese(self, ctx, word):
        url = "https://jisho.org/api/v1/search/words?keyword="
        response = requests.get(url + word)

        content = response.json()

        if content["meta"]["status"] != 200:
            await ctx.send("Error: Could not communicate with API")
            return

        if len(content["data"]) == 0:
            await ctx.send("")

        print(content["data"][0]["jlpt"])

        output = "Kanji: " + (content["data"][0]["japanese"][0]["word"]) + "\t" \
                 + "Hiragana: " + (content["data"][0]["japanese"][0]["reading"])

        await ctx.send(output)


def setup(client):
    client.add_cog(GifSpam(client))
