import os
import random
import urllib
import requests
from urllib import parse
from discord.ext import commands
from dotenv import load_dotenv


class GifSpam(commands.Cog):

    load_dotenv(".env")

    def __init__(self, client):
        self.client = client
        self.gif_on = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.gif_on:
            await self.post_gif(message)

    @commands.command()
    async def gif(self, ctx):
        self.gif_on = False if self.gif_on else True

    async def post_gif(self, message):

        ctx = await self.client.get_context(message)
        word = message.content

        url = "http://api.giphy.com/v1/gifs/search?"

        params = urllib.parse.urlencode({
            "q": f"{word}",
            "api_key": os.getenv("GIF_API_KEY"),
            "limit": "20",
            "rating": "pg"
        })

        response = (requests.get(url + params))
        gif = response.json()
        gif_data = gif["data"]

        if len(gif_data) == 0:
            return

        await ctx.send(random.choice(gif_data)["url"])


def setup(client):
    client.add_cog(GifSpam(client))
