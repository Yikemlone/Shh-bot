import asyncio
import os
import youtube_dl
import discord
from googleapiclient.discovery import build
from discord import ClientException
from discord.ext import commands
from dotenv import load_dotenv


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channel = None
        self.voice_client = None
        self.YT_DL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    async def move_vc(self, ctx, vc_name):
        await self.leave(ctx)
        self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
        self.voice_client = await self.channel.connect()

    async def is_in_vc(self, ctx, vc_name):
        if self.channel is not None and vc_name != self.channel and self.voice_client.is_connected():
            await self.move_vc(ctx, vc_name)
            return True
        else:
            return False

    async def join(self, ctx: discord):
        try:
            vc_name = ctx.author.voice.channel.name

            if not await self.is_in_vc(ctx, vc_name):
                self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
                self.voice_client = await self.channel.connect()

        except ClientException:
            await ctx.send(f"{ctx.author.mention} the bot is already the current VC.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} the bot took too long to join the VC.")
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} you must be in a VC to play music.")

    @commands.command()
    async def leave(self, ctx):
        self.voice_client.stop()
        await self.voice_client.disconnect()

    @staticmethod
    def get_link(url):
        load_dotenv(".env")

        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        url = url.replace(" ", "+")

        request = youtube.search().list(
            part="snippet",
            maxResults=1,
            q=f"{url}"
        )

        request = request.execute()
        video_id = request["items"][0]["id"]["videoId"]

        return f"https://www.youtube.com/watch?v={video_id}"

    @commands.command()
    async def play(self, ctx, *, url):
        # There is a bug where the bot will leave the VC if !play is called again when it's already in the same VC.
        # We will need to check and make sure the bot is not playing before we play a song, and if it is, we should add
        # it to a queue so it can be played next.
        #   * Make it not leave the VC if it's the same VC
        #   * Make queue

        if "http" not in url:
            url = self.get_link(url)

        await self.join(ctx)

        if self.channel is not None:
            with youtube_dl.YoutubeDL(self.YT_DL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info["formats"][0]["url"]
                source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
                self.voice_client.play(source)

    @commands.command()
    async def pause(self, ctx):
        self.voice_client.pause()


def setup(client):
    client.add_cog(Music(client))
