import os
import urllib
import requests
from urllib import parse
from discord.ext import commands
from dotenv import load_dotenv


class GifSpam(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.gifOn = True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        ctx = await self.client.get_context(message)

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
        gifDataDict = gifData[0]

        await ctx.send(gifDataDict["url"])


def setup(client):
    client.add_cog(GifSpam(client))
