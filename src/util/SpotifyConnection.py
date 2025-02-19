# from util import APIConnection
import os
import urllib
import aiohttp
import dotenv
import requests
from urllib import parse
from util.logger import logging

logger = logging.getLogger("shh-bot")

class SpotifyConnection():

    @staticmethod
    async def get_data(data):
        try:
            data = data.replace(" ", "+")
            """Returns a tuple with song name and artist."""
            URL = "https://api.spotify.com/v1/search?"

            request = urllib.parse.urlencode({
                "q": f"{data}",
                "type": "track,artist",
                "limit": "1"
            })

            # Use aiohttp for async HTTP requests
            async with aiohttp.ClientSession() as session:
                header = {"Authorization": f"Bearer {os.getenv('SPOTIFY_TOKEN')}"}
                async with session.get(URL + request, headers=header) as response:
                    response_data = await response.json()

            artist_name = response_data["tracks"]["items"][0]["album"]["artists"][0]["name"]
            song_name = response_data["tracks"]["items"][0]["album"]["name"]

            song_details = {
                "name": artist_name,
                "song": song_name,
            }
            
            return song_details

        except KeyError:
            # This will nearly always be a KeyError, need to figure out why it's happening
            SpotifyConnection.set_spotify_auth()
            logger.info("Token expired, setting new token.")
            return await SpotifyConnection.get_data(data)
        except Exception as ex:
            logger.error(ex)

    @staticmethod
    def set_spotify_auth():
        """Will set a new token of authorization from spotify."""
        URL = "https://accounts.spotify.com/api/token"
        CLIENT_ID = os.getenv("SPOTIFY_ID")
        CLIENT_SECRET = os.getenv("SPOTIFY_SECRET")

        body_params = {"grant_type": "client_credentials"}
        response = requests.post(URL, data=body_params, auth=(CLIENT_ID, CLIENT_SECRET))
        data = response.json()

        os.environ["SPOTIFY_TOKEN"] = data["access_token"]

        if response.status_code == 200:
            dotenv.set_key(".env", "SPOTIFY_TOKEN", os.environ["SPOTIFY_TOKEN"])
        else:
            return

    @staticmethod
    def get_random_song(artist):
        """This will return a song that from the artist passed in."""
        pass
