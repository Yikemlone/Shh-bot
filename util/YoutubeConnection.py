import os
from util.Connection import Connection
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv(".env")


class YouTubeConnection(Connection):

    @staticmethod
    def get_data(data):

        YOUTUBE = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

        try:
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
