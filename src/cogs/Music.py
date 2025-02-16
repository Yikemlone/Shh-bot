import asyncio
import os
import yt_dlp as youtube_dl	
import discord
from discord import ClientException
from discord.ext import commands
from util.YouTubeConnection import YouTubeConnection
from util.SpotifyConnection import SpotifyConnection 


class Music(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.voice_client = None
        self.song_source = None
        self.queue = []
        self.looping = False
        self.radio_songs = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        
        self.YT_DL_OPTIONS  = {
            'format': 'bestaudio[ext=m4a]/bestaudio',  # Prioritize direct audio formats
            'noplaylist': True,  # Only process a single video
            'quiet': True,  # Suppress extra output
        }

        self.ytdl = youtube_dl.YoutubeDL(self.YT_DL_OPTIONS)
        self.FFMPEG_EXE_PATH = "ffmpeg-2025\\bin\\ffmpeg.exe"


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
                self.channel = ctx.author.voice.channel
                self.voice_client = await self.channel.connect()

            elif vc_name != str(self.channel):
                await self.move_vc(ctx, vc_name)

        except ClientException:
            await ctx.send(f"{ctx.author.mention} the bot is already the current VC.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} the bot took too long to join the VC.")
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} you must be in a VC to play music.")
        except Exception as ex:
            print(ex)


    @discord.app_commands.command(name="leave", description="This will make the bot leave the VC.")
    async def leave(self, ctx):
        """The bot will leave the VC it is currently in."""
        self.voice_client.stop()
        await self.voice_client.disconnect()


    @discord.app_commands.command(name="play", description="This will play the song that is passed in.")
    @discord.app_commands.describe(url="The url of the song you want to play. Can be song name.")
    async def play(self, interaction : discord.Interaction, url : str):
        """Adds the song to a queue list, joins the VC the user is in and then it will try to play the songs in the queue."""

        if "http" not in url:
            url = await self.get_link(interaction, url)

        if url is not None:
            self.queue.append(url)

        print(self.radio_songs)

        await self.join(interaction)
        await self.play_song(interaction, self.queue[0])


    @discord.app_commands.command(name="skip", description="This will skip the current song and play the next song in the queue.")
    async def skip(self, interaction: discord.Interaction):
        """Updates the queue and plays the next song."""

        if len(self.queue) < 2:
            await interaction.response.send_message(f"{interaction.author.mention} no more songs in queue. Queue some with \"!play\" *song name*.")
            return

        self.voice_client.stop()
        self.update_queue()

        await self.play_song(interaction, self.queue[0])


    @discord.app_commands.command(name="pause", description="This will pause the song that is currently playing.")
    async def pause(self, ctx):
        """Pauses the song that is currently playing."""
        self.voice_client.pause()


    @discord.app_commands.command(name="resume", description="This will resume a song that was playing.")
    async def resume(self, ctx):
        """Resumes a song that was playing."""
        self.voice_client.play(self.song_source)


    @discord.app_commands.command(name="loop", description="This will loop the songs in the queue.")    
    async def loop(self, interaction: discord.Interaction):
        """Will set the bot to loop the songs in the queue."""

        if self.looping:
            self.looping = False
            self.queue = []
            await interaction.response.send_message(f"{interaction.author.mention} no longer looping songs.")
        else:
            self.looping = True
            await interaction.response.send_message(f"{interaction.author.mention} looping songs.")


    @discord.app_commands.command(name="queue", description="This will print out the current queue.")
    async def queue(self, interaction: discord.Interaction):
        """Will print out the queue as a discord embed."""
        # image = discord.File(os.path.join("text_files", "Skelly-thumbs-up.gif"), filename="Skelly-thumbs-up.gif")

        embed = discord.Embed(
            title="Song Queue",
            color=discord.Color.gold(),
        )

        for index, song in enumerate(self.radio_songs):
            if song is not None:
                artist_name = self.radio_songs[index]["name"]
                song_name = self.radio_songs[index]["song"]
                embed.add_field(name="Artist", value=artist_name, inline=True)
                embed.add_field(name="Song", value=song_name, inline=False)

        # await ctx.send(file=image)
        await interaction.response.send_message(embed=embed)


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
                song_url = song_information["url"]
                self.song_source = discord.FFmpegPCMAudio(song_url, **self.FFMPEG_OPTIONS, executable=self.FFMPEG_EXE_PATH) 
                self.voice_client.play(self.song_source)
                await asyncio.sleep(song_information["duration"] + 2)
            
            self.update_queue()

            if len(self.queue) > 0:
                await self.play_song(ctx, self.queue[0])

        except ClientException as ex:
            print(ex)
            await ctx.send(f"{ctx.author.mention} something went wrong with playing the song you requested.")
        except Exception as ex:
            print(ex)
            await ctx.send(f"{ctx.author.mention} unknown error with playing a song.")


    def radio_mode(self):
        """This will be be called when the bot goes into radio mode. It will play songs from the same artists or genres
        that were played this session."""
        pass


    def store_for_radio_mode(self, song):
        """This will get the artist and track for the radio mode and store them in a list."""
        self.radio_songs.append(SpotifyConnection.get_data(song))


async def setup(bot):
    await bot.add_cog(Music(bot))
