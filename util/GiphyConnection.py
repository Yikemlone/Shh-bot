import os
import urllib
import requests
from urllib import parse
from util.Connection import Connection


class GiphyConnection(Connection):

    @staticmethod
    def get_data(data):
        word = data.content

        url = "http://api.giphy.com/v1/gifs/search?"

        params = urllib.parse.urlencode({
            "q": f"{word}",
            "api_key": os.getenv("GIF_API_KEY"),
            "limit": "20",
            "rating": "pg"
        })

        response = (requests.get(url + params))
        gif = response.json()
        gif_data = gif["data"]

        return gif_data
