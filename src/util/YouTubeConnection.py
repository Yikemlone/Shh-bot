# from util import APIConnection
import os 
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv(".env")

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
            print(ex)
