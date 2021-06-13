import os
import discord
import json
import urllib
from urllib import parse
from urllib import request
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

        await self.client.process_commands(message)

        ctx = await self.client.get_context(message)

        if self.gifOn:
            await ctx.send("We are inside gif on if")
            self.postGif("hey")

    @commands.command()
    async def gif(self, ctx):
        if self.gifOn:
            self.gifOn = False
        else:
            self.gifOn = True

    def postGif(self, message):
        load_dotenv(".env")

        url = "http://api.giphy.com/v1/gifs/search?%"

        params = urllib.parse.urlencode({
            "q": "Happy",
            "api_key": os.getenv("GIF_API_KEY"),
            "limit": "1"
        })

        with urllib.request.urlopen("".join(url + params)) as response:
            data = json.loads(response.read())

        print(json.dumps(data, sort_keys=True, indent=4))


def setup(client):
    client.add_cog(GifSpam(client))
