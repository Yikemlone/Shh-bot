# from util import APIConnection
import os 
from googleapiclient.discovery import build
from util.logger import logging

logger = logging.getLogger("shh-bot")

class YouTubeConnection():

    @staticmethod
    def get_data(data):
        try:
            YOUTUBE = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

            request = YOUTUBE.search().list(
                part="snippet",
                maxResults=1,
                q=f"{data}"
            )

            response = request.execute()
            video_id = response["items"][0]["id"]["videoId"]

            return f"https://www.youtube.com/watch?v={video_id}"

        except IndexError:
            return None
        except Exception as ex:
            logger.info(ex)
