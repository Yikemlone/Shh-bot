import discord
from discord.ext import commands


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        vc = discord.utils.get(ctx.guild.voice_channels, name="General")
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        # print(voice)

        await vc.connect()
        # if await voice.is_connected() is None:

    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await voice.disconnect()


def setup(client):
    client.add_cog(Music(client))
