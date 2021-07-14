import asyncio

import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from util.CustomHelpCommand import CustomHelpCommand

load_dotenv(".env")

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.do_not_disturb,
                      help_command=CustomHelpCommand(), voice_client=discord.VoiceClient)

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "Nsfw.py":
        client.load_extension(f"cogs.{filename[:-3]}")


def is_server_owner(ctx):
    if ctx.author.id == 401415617032486922:
        return True


@client.event
async def on_message(message: discord):
    if message.author.bot:
        return

    await client.process_commands(message)


@client.command()
# @client.check(isServerOwner)
async def load(ctx, extension: str):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension: str):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension: str):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


@client.command(aliases=["type"])
async def bot_type(ctx):
    messages = {
        "avatar": ctx.author.avatar_url,
        "message": "This you?",
        "GIF": "https://tenor.com/view/kermit-the-frog-drive-driving-gif-12873213"
    }

    for message in messages:
        await ctx.trigger_typing()
        await asyncio.sleep(1.5)
        await ctx.send(messages[message])


# Bot token
client.run(os.getenv('BOT_TOKEN'))
