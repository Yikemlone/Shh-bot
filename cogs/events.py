from discord.ext import commands
from pprint import pprint


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.currentUser = ""

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if self.currentUser == "":
            self.currentUser = user
            return

        if user is self.currentUser:
            await channel.send(f"{user} stop typing.")

        # # await asyncio.sleep(20)
        # timeAfter = datetime.datetime.now().time()
        #
        # if timeAfter > beforeTime and currentUser is user:
        #     await channel.send(f"{user} what are you typing? Stop it.")


def setup(client):
    client.add_cog(Events(client))

