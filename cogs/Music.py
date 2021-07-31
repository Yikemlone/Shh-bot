import asyncio
import os
import youtube_dl
import discord
from googleapiclient.discovery import build
from discord import ClientException
from discord.ext import commands
from dotenv import load_dotenv


class Music(commands.Cog):

    load_dotenv(".env")

    def __init__(self, client):
        self.client = client
        self.channel = None
        self.voice_client = None
        self.YT_DL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.queue = []
        self.song_source = None
        self.looping = False

    async def move_vc(self, ctx, vc_name):
        """Will leave current VC, to a new VC."""
        await self.leave(ctx)
        self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
        self.voice_client = await self.channel.connect()

    def update_queue(self):
        """Will pop the the first element out of the queue."""
        if len(self.queue) > 0:
            if not self.looping:
                self.queue.pop(0)

            elif self.looping:
                self.queue.append(self.queue[0])
                self.queue.pop(0)

    async def join(self, ctx):
        """The bot will try to connect to the VC the user is in."""
        try:
            vc_name = ctx.author.voice.channel.name

            if self.channel is None:
                self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
                self.voice_client = await self.channel.connect()

            elif vc_name != str(self.channel):
                await self.move_vc(ctx, vc_name)

        except ClientException:
            await ctx.send(f"{ctx.author.mention} the bot is already the current VC.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} the bot took too long to join the VC.")
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} you must be in a VC to play music.")

    @commands.command()
    async def leave(self, ctx):
        """The bot will leave the VC it is currently in."""
        self.voice_client.stop()
        await self.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Adds the song to a queue, joins the VC and then it will try to play the songs in the queue."""
        if "http" not in url:
            url = await self.get_link(ctx, url)

        if url is not None:
            self.queue.append(url)

        await self.join(ctx)
        await self.play_song(ctx, self.queue[0])
        print(self.queue)

    @commands.command()
    async def skip(self, ctx):
        """Updates the queue and plays the next song."""
        if len(self.queue) > 1:
            self.voice_client.stop()
            self.update_queue()
            await self.play_song(ctx, self.queue[0])
        else:
            await ctx.send(f"{ctx.author.mention} no more songs in queue. Add more with \"!play\".")

    @commands.command()
    async def pause(self, ctx):
        """Pauses the song that is currently playing."""
        self.voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Resumes a song that was playing."""
        self.voice_client.play(self.song_source)

    @commands.command()
    async def loop(self, ctx):
        """Will set the bot to loop the songs in the queue."""

        # This may cause an issue where if the no longer want to loop, it will still play the most recent song last.
        # A way to solve this is to have two separate queues and interchange them as needed.

        if self.looping:
            self.looping = False
            await ctx.send(f"{ctx.author.mention} now no longer looping songs.")
        else:
            self.looping = True
            await ctx.send(f"{ctx.author.mention} now looping songs.")

    @staticmethod
    async def get_link(ctx, video_name):
        """Returns a link of the top search video with the name passed in."""
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        video_name = video_name.replace(" ", "+")

        try:
            request = youtube.search().list(
                part="snippet",
                maxResults=1,
                q=f"{video_name}"
            )

            request = request.execute()
            video_id = request["items"][0]["id"]["videoId"]

            return f"https://www.youtube.com/watch?v={video_id}"

        except IndexError:
            await ctx.send(f"{ctx.author.mention} could not find the song you were looking for.")

            return None

    async def play_song(self, ctx, song):
        """Try to play the song that was passed in."""
        if not self.voice_client.is_playing():
            try:
                with youtube_dl.YoutubeDL(self.YT_DL_OPTIONS) as ydl:
                    info = ydl.extract_info(song, download=False)
                    song_url = info["formats"][0]["url"]
                    self.song_source = await discord.FFmpegOpusAudio.from_probe(song_url, **self.FFMPEG_OPTIONS)
                    self.voice_client.play(self.song_source)

                    await asyncio.sleep(info["duration"] + 2)

                    self.update_queue()

                    if len(self.queue) > 0:
                        await self.play_song(ctx, self.queue[0])

            except ClientException:
                await ctx.send(f"{ctx.author.mention} something went wrong with playing the song you requested.")


def setup(client):
    client.add_cog(Music(client))
