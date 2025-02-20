import asyncio
import yt_dlp as youtube_dl	
import discord
from discord import ClientException
from discord.ext import commands
from util.youtubeconnection import YouTubeConnection
from util.spotifyconnection import SpotifyConnection 
from util.logger import logging

logger = logging.getLogger("shh-bot")


class Music(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.channel = None
        self.voice_client : discord.VoiceClient = None
        self.song_source = None
        self.song_queue = []
        self.current_song = {}
        self.looping = False
        self.radio_songs = [] # This was intened to be used for radio mode.
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        
        self.YT_DL_OPTIONS  = {
            'format': 'bestaudio[ext=m4a]/bestaudio',  # Prioritize direct audio formats
            'noplaylist': True,  # Only process a single video
            'quiet': True,  # Suppress extra output
        }

        self.ytdl = youtube_dl.YoutubeDL(self.YT_DL_OPTIONS)
        self.FFMPEG_EXE_PATH = "ffmpeg-2025\\bin\\ffmpeg.exe"


    async def move_vc(self, interaction: discord.Interaction, vc_name): 
        """Will leave current VC, to a new VC."""
        await self.leave(interaction)
        self.channel = discord.utils.get(interaction.guild.voice_channels, name=vc_name)
        self.voice_client = await self.channel.connect()


    def update_queue(self):
        """Will pop the first song out of the queue and update current_song."""
        if len(self.song_queue) == 0:
            logger.info(f"No more songs in queue.")
            self.current_song = {}
            return

        if self.looping:
            self.song_queue.append(self.song_queue[0]) 

        self.current_song = self.song_queue[0]
        self.song_queue.pop(0)
        logger.info(f"Current song queue: {self.song_queue}")


    async def join_voice_channel(self, interaction : discord.Interaction):
        """The bot will try to connect to the VC the user is in."""
        if interaction.user.voice is None:
            return False
        
        vc_name = interaction.user.voice.channel.name

        try:
            logger.info(f"Trying to join VC {vc_name}")

            if self.channel is None:
                self.channel = interaction.user.voice.channel
                self.voice_client = await self.channel.connect()
            elif vc_name != str(self.channel):
                await self.move_vc(interaction, vc_name)

            return True
        
        except ClientException:
            logger.warning("ClientException: User is not in a VC.")
            # await interaction.response.send_message(f"{interaction.user.mention} the bot is already the current VC.")
        except asyncio.TimeoutError:
            logger.warning("TimeoutError: Bot took too long to join VC.")
            # await interaction.response.send_message(f"{interaction.user.mention} the bot took too long to join the VC.")
        except AttributeError:
            logger.warning("AttributeError: User is not in a VC.")
            # await interaction.response.send_message(f"{interaction.user.mention} you must be in a VC to play music.")
        except Exception as ex:
            logger.error(ex)


    @discord.app_commands.command(name="leave", description="This will make the bot leave the VC.")
    async def leave(self, interaction : discord.Interaction):
        """The bot will leave the VC it is currently in."""
        self.voice_client.stop()
        self.voice_client = await self.voice_client.disconnect() # TODO: See if I need to return this and set it.
        await interaction.response.send_message(f"{interaction.user.mention} has left the {self.channel} VC.")
        logger.info(f"Bot has left the {self.channel} VC.")
        self.channel = None
        self.song_queue = []
        self.current_song = {}


    @discord.app_commands.command(name="play", description="This will play the song that is passed in.")
    @discord.app_commands.describe(name="The name of the song you want to play. Can be a URL.")
    # TODO: Add a artist optional argument.
    # @discord.app_commands.option(name="artist", type=3, description="The name of the song you want to play. Can be a URL.")
    async def play(self, interaction : discord.Interaction, name : str):
        """Adds the song to a queue list, joins the VC the user is in and then it will try to play the songs in the queue."""
        try:
            await interaction.response.defer()
            isInChannel = await self.join_voice_channel(interaction)
            
            if isInChannel:
                message = await self.try_to_play_song(interaction, name)
                await interaction.followup.send(message)
            else:
                await interaction.followup.send(f"{interaction.user.mention} you must be in a VC to play music.")

        except Exception as ex:
            logger.error(ex)


    @discord.app_commands.command(name="skip", description="This will skip the current song and play the next song in the queue.")
    async def skip(self, interaction: discord.Interaction):
        """Updates the queue and plays the next song."""

        if len(self.song_queue) == 0:
            await interaction.response.send_message(f"{interaction.user.mention} no more songs in queue. Queue some with the /queue command and a *song name*.")
            return

        logger.info(f"Playing next song in queue: {self.current_song}")
        self.voice_client.stop()
        await interaction.response.send_message(f"{interaction.user.mention} skipping **{self.current_song["song"]}** by **{self.current_song["name"]}**. Now playing **{self.song_queue[0]['song']}** by **{self.song_queue[0]['name']}**.")
        logger.info(f"Playing next song in queue: {self.current_song}")
        self.play_current_song(self.current_song["URL"])


    @discord.app_commands.command(name="pause", description="This will pause the song that is currently playing.")
    async def pause(self, interaction: discord.Interaction):
        """Pauses the song that is currently playing."""
        self.voice_client.pause()
        await interaction.response.send_message(f"{interaction.user.mention} pausing **{self.current_song["song"]}** by **{self.current_song["name"]}**.")


    @discord.app_commands.command(name="resume", description="This will resume a song that was playing.")
    async def resume(self, interaction: discord.Interaction):
        """Resumes a song that was playing."""
        self.voice_client.play(self.song_source)
        await interaction.response.send_message(f"{interaction.user.mention} resuming **{self.current_song["song"]}** by **{self.current_song["name"]}**.")


    @discord.app_commands.command(name="loop", description="This will loop the current songs in the queue.")    
    async def loop(self, interaction: discord.Interaction):
        """Will set the bot to loop the songs in the queue."""
        if self.looping:
            self.looping = False
            self.song_queue = []
            await interaction.response.send_message(f"{interaction.user.mention} no longer looping songs.")
        else:
            self.looping = True
            await interaction.response.send_message(f"{interaction.user.mention} looping songs.")

        logger.info(f"Song queue looping: {self.looping}")


    @discord.app_commands.command(name="queue", description="Displays a list of current songs in the queue.")
    async def queue(self, interaction: discord.Interaction):
        """Will send the queue as a discord embed."""
        # image = discord.File(os.path.join("text_files", "Skelly-thumbs-up.gif"), filename="Skelly-thumbs-up.gif")
        if len(self.song_queue) == 0 and not self.current_song:
            await interaction.response.send_message(f"{interaction.user.mention} no songs in queue. Queue some with the /play command and a *song name*.")
            return
        
        embed = discord.Embed(
            title="Song Queue",
            color=discord.Color.red(),
        )
        
        embed.add_field(name=":musical_note: Now Playing", value=f"**{self.current_song['song']}** by **{self.current_song['name']}**", inline=False)

        for index, song in enumerate(self.song_queue):
            if song is not None:
                artist_name = self.song_queue[index]["name"]
                song_name = self.song_queue[index]["song"]
                embed.add_field(name=f"#{index + 1}", value=f"**{song_name}** by **{artist_name}**", inline=True)

        # await ctx.send(file=image)
        await interaction.response.send_message(embed=embed)


    async def get_link(self, name):
        """Returns a string as a link of the top search video with the name passed in. Else it returns None"""
        self.store_for_radio_mode(name)
        link = await YouTubeConnection.get_data(name)

        if link is None:
            logger.error(f"Error getting link for {name}")
            # await interaction.response.send_message(f"{interaction.user.mention} there was an error getting that song.")
        return link
    

    async def try_to_play_song(self, interaction : discord.Interaction, name):
        """Will try to play the song that was passed in. If the bot is already playing a song, it will add the song to the queue."""
        try:
            if self.voice_client.is_playing():
                self.song_queue.append(await self.get_song_details(name))
                return f"{interaction.user.mention} the bot is already playing a song. Added {self.song_queue[-1]["URL"]} to queue."
            elif self.voice_client.is_paused():
                self.song_queue.append(await self.get_song_details(name))
                self.voice_client.resume()
                return f"{interaction.user.mention} resuming {self.current_song["song"]} by {self.current_song["name"]}. Added {self.song_queue[-1]["URL"]} to queue."
            else:
                self.current_song = await self.get_song_details(name)

            self.play_current_song(self.current_song["URL"])
            
            return f"{interaction.user.mention} now playing **{self.current_song['song']}** by **{self.current_song['name']}**. {self.current_song["URL"]}"
        
        except Exception as ex:
            logger.error(f"An unknown exception occurred: {ex}")
            return f"{interaction.user.mention} unknown error with playing a song."
    

    def play_current_song(self, song_url):
        """Will play the song that was passed in."""
        try:
            with youtube_dl.YoutubeDL(self.YT_DL_OPTIONS) as ydl:
                song_information = ydl.extract_info(song_url, download=False)
                song_url = song_information["url"]
                self.song_source = discord.FFmpegPCMAudio(song_url, **self.FFMPEG_OPTIONS, executable=self.FFMPEG_EXE_PATH) 

            def after_playback(error):
                if error:
                    logger.error(f"Playback error: {error}")
                
                self.update_queue()

                if self.current_song:
                    logger.info(f"Playing next song in queue: {self.current_song["URL"]}")
                    self.play_current_song(self.current_song["URL"])

            self.voice_client.play(self.song_source, after=after_playback)

        except Exception as ex:
            logger.error(f"Error in play_current_song: {ex}")


    def radio_mode(self):
        """This will be be called when the bot goes into radio mode. It will play songs from the same artists or genres
        that were played this session."""
        pass

    async def get_song_details(self, song_name):
        """This will get the artist and track for the radio mode and store them in a list."""
        url = None
        song_details = await SpotifyConnection.get_data(song_name)

        if "http" not in song_name:
            url = await self.get_link(song_name)

        if url is not None:
            return {"URL": url, "name": song_details["name"], "song": song_details["song"]}
        else:
            logger.error(f"Error getting song details for {song_name}")
            return None #TODO: See what happens in this scenario.


    def store_for_radio_mode(self, song):
        """This will get the artist and track for the radio mode and store them in a list."""
        self.radio_songs.append(SpotifyConnection.get_data(song))


async def setup(bot):
    await bot.add_cog(Music(bot))
