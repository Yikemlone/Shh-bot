import asyncio
import os
import youtube_dl
import discord
from discord import ClientException
from discord.ext import commands
from dotenv import load_dotenv
from util.YouTubeConnection import YouTubeConnection
from util.SpotifyConnection import SpotifyConnection 


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
            # if self.channel is not None:
            self.channel = discord.utils.get(ctx.guild.voice_channels, name=vc_name)
            self.voice_client = await self.channel.connect()

            # elif vc_name != str(self.channel):
            #     await self.move_vc(ctx, vc_name)

        except ClientException:
            await ctx.send(f"{ctx.author.mention} the bot is already the current VC.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} the bot took too long to join the VC.")
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} you must be in a VC to play music.")
        except Exception as ex:
            print(ex)

    @commands.command(aliases=["l"])
    async def leave(self, ctx):
        """The bot will leave the VC it is currently in."""
        self.voice_client.stop()
        await self.voice_client.disconnect()

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, url):
        """Adds the song to a queue list, joins the VC the user is in and then it will try to play the songs in the
        queue."""
        if "http" not in url:
            url = await self.get_link(ctx, url)

        if url is not None:
            self.queue.append(url)

        print(self.radio_songs)

        await self.join(ctx)
        await self.play_song(ctx, self.queue[0])

    @commands.command(aliases=["s"])
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
            await ctx.send(f"{ctx.author.mention} no longer looping songs.")
        else:
            self.looping = True
            await ctx.send(f"{ctx.author.mention} looping songs.")

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        """Will print out the queue as a discord embed."""
        image = discord.File(os.path.join("text_files", "Skelly-thumbs-up.gif"), filename="Skelly-thumbs-up.gif")

        embed = discord.Embed(
            title="Song Queue",
            color=discord.Color.gold(),
        )

        for index, song in enumerate(self.radio_songs):
            artist_name = self.radio_songs[index]["name"]
            song_name = self.radio_songs[index]["song"]
            embed.add_field(name="Artist", value=artist_name, inline=True)
            embed.add_field(name="Song", value=song_name, inline=False)

        await ctx.send(file=image)
        await ctx.send(embed=embed)

    async def get_link(self, ctx, name):
        """Returns a string as a link of the top search video with the name passed in. Else it returns None"""
        name = name.replace(" ", "+")
        self.store_for_radio_mode(name)
        link = YouTubeConnection.get_data(name)

        if link is None:
            ctx.send(f"{ctx.author.mention} there was an error getting that song.")

        return link

    async def play_song(self, ctx, song):
        """Will try to play the song that was passed in."""
        try:
            if self.voice_client.is_playing():
                return

            with youtube_dl.YoutubeDL(self.YT_DL_OPTIONS) as ydl:
                song_information = ydl.extract_info(song, download=False)
                song_url = song_information["formats"][0]["url"]
                self.song_source = await discord.FFmpegOpusAudio.from_probe(song_url, **self.FFMPEG_OPTIONS)
                self.voice_client.play(self.song_source)
                await asyncio.sleep(song_information["duration"] + 2)

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
        """This will get the artist and track for the radio mode and store them in a list."""
        self.radio_songs.append(SpotifyConnection.get_data(song))


async def setup(client):
    await client.add_cog(Music(client))
