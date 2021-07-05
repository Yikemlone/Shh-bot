from discord.ext import commands
from pprint import pprint
import asyncio
import datetime


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.currentUser = ""
        self.timeStartedTyping = None

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if self.currentUser == "":
            self.currentUser = user
            self.timeStartedTyping = when.time()
            await asyncio.sleep(20)

            return

        if user is self.currentUser:
            await channel.send(f"{user} stop typing.")
        else:
            self.currentUser = ""


def setup(client):
    client.add_cog(Events(client))

