
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from util.CustomHelpCommand import CustomHelpCommand
import asyncio

load_dotenv(".env")
intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.do_not_disturb,
                      help_command=CustomHelpCommand(), voice_client=discord.VoiceClient)

async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
           await client.load_extension(f"cogs.{filename[:-3]}")


# def is_server_owner(ctx):
#     if ctx.message.author.id == 401415617032486922:
#         return True


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)


@client.command()
# @client.check(is_server_owner)
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")


@client.command()
# @client.check(is_server_owner)
async def unload(ctx, extension):
   await client.unload_extension(f"cogs.{extension}")


@client.command()
# @client.check(is_server_owner)
async def reload(ctx, extension):
   await client.unload_extension(f"cogs.{extension}")
   await client.load_extension(f"cogs.{extension}")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())


