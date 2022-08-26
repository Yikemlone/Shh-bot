import random
from discord.ext import commands
from util.GiphyConnection import GiphyConnection


class GifSpam(commands.Cog):


    def __init__(self, client):
        self.client = client
        self.gif_on = False

    @commands.Cog.listener()
    async def on_message(self, message):
        """Will check if the bot should post gifs."""
        if message.author.bot:
            return

        if self.gif_on:
            await self.post_gif(message)

    @commands.command()
    async def gif(self, ctx):
        """Toggles the bot on and off from posting gifs."""
        self.gif_on = False if self.gif_on else True

    async def post_gif(self, message):
        """Will post a gif in the server"""
        ctx = await self.client.get_context(message)
        word = message.content
        gif_data = GiphyConnection.get_data(word)

        if len(gif_data) == 0:
            return

        await ctx.send(random.choice(gif_data)["url"])


async def setup(client):
    await client.add_cog(GifSpam(client))