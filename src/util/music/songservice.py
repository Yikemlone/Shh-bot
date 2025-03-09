import yt_dlp as youtube_dl	
import os
from discord import FFmpegPCMAudio
from util.apiconnection.spotifyconnection import SpotifyConnection
from util.apiconnection.youtubeconnection import YouTubeConnection
from util.logger import logging, SHH_BOT

logger = logging.getLogger(SHH_BOT)

class SongService():

    def __init__(self):
        self.FFMPEG_OPTIONS : dict  = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.YT_DL_OPTIONS : dict = {'format': 'bestaudio[ext=m4a]/bestaudio', 'noplaylist': True, 'quiet': True} 
        self.FFMPEG_EXE_PATH : str =  os.path.join("ffmpeg-2025", "bin", "ffmpeg.exe") 
        self.song_source : FFmpegPCMAudio = None


    def get_song_source(self) -> FFmpegPCMAudio:
        return self.song_source
    
    
    def prep_soung_source(self, song_url):
        """Will play the song that was passed in."""
        try:
            with youtube_dl.YoutubeDL(self.YT_DL_OPTIONS) as ydl:
                song_information = ydl.extract_info(song_url, download=False)
                song_url = song_information["url"]
                self.song_source = FFmpegPCMAudio(song_url, **self.FFMPEG_OPTIONS, executable=self.FFMPEG_EXE_PATH) 
        except Exception as ex:
            logger.error(f"Error in prep_soung_source: {ex}")


    async def get_song_details(self, song_name) -> dict:
        url = None
        song_details = await SpotifyConnection.get_data(song_name)

        if "http" not in song_name:
            url = await self.get_link(song_name)

        if url is not None:
            return {"URL": url, "name": song_details["name"], "song": song_details["song"]}
        else:
            logger.error(f"Error getting song details for {song_name}")
            return None #TODO: See what happens in this scenario.


    async def get_link(self, name : str) -> str:
        """Returns a string as a link of the top search video with the name passed in. Else it returns None"""
        link = await YouTubeConnection.get_data(name)

        if link is None:
            logger.error(f"Error getting link for {name}")

        return link