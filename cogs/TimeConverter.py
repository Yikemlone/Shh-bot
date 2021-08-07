import discord
import datetime
from discord.ext import commands


class TimeConverter(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        smush_emoji = discord.utils.get(self.client.emojis, name="smush")

        if self.has_time(message.content):
            await message.add_reaction(smush_emoji)

    @staticmethod
    def has_time(message):
        """Will return true if the message has a valid time."""
        print(message)

    async def validate_time(self, message):
        """Will check the if the time in the message is valid."""
        pass

    async def send_user_converted_time(self, user):
        """Will send the user who reacted the time converted to their local time."""
        pass

    async def convert_time(self, time):
        """Returns the time passed in converted to user local time."""

def setup(client):
    client.add_cog(TimeConverter(client))
