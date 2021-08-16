import os
import urllib
import dotenv
import requests
from urllib import parse
from util.Connection import Connection


class SpotifyConnection(Connection):

    @staticmethod
    def get_data(data):
        """Returns a tuple with song name and artist."""
        URL = "https://api.spotify.com/v1/search?"

        request = urllib.parse.urlencode({
            "q": f"{data}",
            "type": "track,artist",
            "limit": "1"
        })

        while True:
            try:
                header = {"Authorization": f"Bearer {os.getenv('SPOTIFY_TOKEN')}"}
                response = requests.get(URL + request, headers=header).json()
                artist_name = response["tracks"]["items"][0]["album"]["artists"][0]["name"]
                song_name = response["tracks"]["items"][0]["album"]["name"]

                song_details = {
                    "name": artist_name,
                    "song": song_name,
                }

                return song_details

            except KeyError:
                SpotifyConnection.set_spotify_auth()

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
