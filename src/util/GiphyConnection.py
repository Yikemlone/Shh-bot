# from util import APIConnection
import os
import urllib
import requests
from urllib import parse
from util.logger import logging

logger = logging.getLogger("shh-bot")

class GiphyConnection():

    @staticmethod
    async def get_data(data):
        try:
            data = data.replace(" ", "+")
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
            logger.info(ex)

        return gif_data
 