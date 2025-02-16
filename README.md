# **Shh! Bot**

## **Summary**

Python version: 3.12.1

This is a bot made for Discord using Discord.py.

To be able to get this bot to work, you must install all the dependencies inside of the requirments.txt file.

``` cmd
pip install -r requirments.txt
```

You must also create a .env file and give it the tokens for the bot and APIs.

API list:

- Spotify
- Giphy
- YouTube

You must also supply your ID and secret for the spotify API to work.

``` .env
BOT_TOKEN= YOUR BOT TOKEN HERE
GIF_API_KEY= GIPHY KEY HERE
YOUTUBE_API_KEY= YOUTUBE KEY HERE
SPOTIFY_TOKEN= SPOTIFY TOKEN HERE
SPOTIFY_ID= SPOTIFY ID HERE 
SPOTIFY_SECRET= SPOTIFY SECRET
```

## **Music Bot**

If you want the music bot to work properly you must have [ffmpeg](https://ffmpeg.org/download.html#build-windows) installed on your machine.

You can put the bin files inside this project and dirrect the bot to it or you can have it in your system path.

```
 self.FFMPEG_EXE_PATH = PATH TO FFMPEG
```

## **Resources**

- [Discord.py Docs](https://discordpy.readthedocs.io/en/stable/)
- [Discord.py GitHub](https://github.com/Rapptz/discord.py)
