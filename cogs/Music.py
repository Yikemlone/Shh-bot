import asyncio
import os
import urllib
import dotenv
import requests
import youtube_dl
import discord
from urllib import parse
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
        self.song_source = None
        self.queue = []
        self.looping = False
        self.radio_songs = []
        self.YT_DL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

    async def move_vc(self, ctx, vc_name):
        """Will leave current VC, to a new VC."""

        await self.leave(ctx)
        self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
        self.voice_client = await self.channel.connect()

    def update_queue(self):
        """Will pop the the first element out of the queue."""

        if not len(self.queue) > 0:
            return

        if self.looping:
            self.queue.append(self.queue[0])

        self.queue.pop(0)

    async def join(self, ctx):
        """The bot will try to connect to the VC the user is in."""

        vc_name = ctx.author.voice.channel.name

        try:
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
        """Adds the song to a queue list, joins the VC the user is in and then it will try to play the songs in the
        queue."""

        if "http" not in url:
            url = await self.get_link(ctx, url)

        if url is not None:
            self.queue.append(url)

        await self.join(ctx)
        await self.play_song(ctx, self.queue[0])

    @commands.command()
    async def skip(self, ctx):
        """Updates the queue and plays the next song."""

        if len(self.queue) < 2:
            await ctx.send(f"{ctx.author.mention} no more songs in queue. Add with \"!play\".")
            return

        self.voice_client.stop()
        self.update_queue()
        await self.play_song(ctx, self.queue[0])

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

        if self.looping:
            self.looping = False
            self.queue = []
            await ctx.send(f"{ctx.author.mention} now no longer looping songs.")
        else:
            self.looping = True
            await ctx.send(f"{ctx.author.mention} now looping songs.")

    async def get_link(self, ctx, video_name):
        """Returns a link of the top search video with the name passed in. Else it returns None"""

        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        video_name = video_name.replace(" ", "+")

        try:

            self.store_for_radio_mode(video_name)

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

        if self.voice_client.is_playing():
            return

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

    def radio_mode(self):
        """This will be be called when the bot goes into radio mode. It will play songs from the same artists or genres
        that were played this session."""
        pass

    def store_for_radio_mode(self, song):
        """This will get the artist and genres for the radio mode and store them in a list."""

        SPOTIFY_URL = "https://api.spotify.com/v1/search?"

        header = {
            "Authorization": f"Bearer {os.getenv('SPOTIFY_TOKEN')}"
        }

        request = urllib.parse.urlencode({
            "q": f"{song}",
            "type": "track,artist",
            "limit": "1"
        })

        try:
            self.set_spotify_auth()

            # if len(os.getenv("SPOTIFY_TOKEN")) <= 0:
            #     return

            response = requests.get(SPOTIFY_URL + request, headers=header)

            data = response.json()

            artist_name = data["tracks"]["items"][0]["album"]["artists"][0]["name"]
            song_name = data["tracks"]["items"][0]["album"]["name"]

            self.radio_songs.append({
                "name": artist_name,
                "song": song_name,
            })

            print(song_name)
            print(artist_name)

        except Exception as ex:
            print(ex)

    @staticmethod
    def set_spotify_auth():
        """Will set a new token of authorization from spotify."""

        spotify_get_url = "https://accounts.spotify.com/authorize"

        request = urllib.parse.urlencode({
            "client_id": f"{os.getenv('SPOTIFY_SECRET')}",
            "response_type": "token",
            "redirect_uri": "http://localhost/"
        })

        try:
            response = requests.get(spotify_get_url + request)

            print(response)

            data = response.json()

            print(data)

            os.environ["SPOTIFY_TOKEN"] = data["access_token"]

            if len(data) > 2:
                dotenv.set_key(".env", "SPOTIFY_TOKEN", os.environ["SPOTIFY_TOKEN"])

        except Exception as ex:
            raise ex


def setup(client):
    client.add_cog(Music(client))
