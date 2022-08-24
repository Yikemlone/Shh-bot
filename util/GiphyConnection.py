# from util import APIConnection
import os
import urllib
import requests
from urllib import parse


class GiphyConnection():

    @staticmethod
    def get_data(data):
        try:
            url = "http://api.giphy.com/v1/gifs/search?"

            params = urllib.parse.urlencode({
                "q": f"{data}",
                "api_key": os.getenv("GIF_API_KEY"),
                "limit": "20",
                "rating": "pg"
            })

            response = (requests.get(url + params))
            gif = response.json()
            gif_data = gif["data"]
        except Exception as ex:
            print(ex)


        return gif_data
 