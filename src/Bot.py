
import discord
import os
import asyncio

from discord import app_commands
from dotenv import load_dotenv
from discord.ext import commands
from calendar import c
from util.CustomHelpCommand import CustomHelpCommand

# Load the environment variables
load_dotenv(".env")

# Define the intents, this is required for the bot to work
intents = discord.Intents.all()
intents.message_content = True


# Define the client
bot = commands.Bot(command_prefix="!", intents=intents,
                      help_command=CustomHelpCommand(), 
                      voice_client=discord.VoiceClient)


async def load_extensions():
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
           await bot.load_extension(f"cogs.{filename[:-3]}")


def is_guild_owner(interaction : discord.Interaction):
    """Decorator to check if the command user is the server owner."""
    if interaction.user.id != interaction.guild.owner_id: return 
    return True


@bot.event
async def on_message(message):
    """ This function will be called whenever a message is sent in the server."""
    if message.author.bot: return
    await bot.process_commands(message)


@bot.tree.command(name="load", description="Loads the COGS into the bot") 
@app_commands.check(is_guild_owner)
async def load(extension):
    await bot.load_extension(f"cogs.{extension}")
    await bot.send("Loaded cog.")


@bot.tree.command(name="unload", description="Unloads the COGS from the bot") 
@app_commands.check(is_guild_owner)
async def unload(extension):
   await bot.unload_extension(f"cogs.{extension}")
   await bot.send("Unloaded cog.")


@bot.tree.command(name="reload", description="Reloads the COGS into the bot") 
@app_commands.check(is_guild_owner)
async def reload(extension):
   await bot.unload_extension(f"cogs.{extension}")
   await bot.load_extension(f"cogs.{extension}")
   await bot.send("Reloaded cog.")


@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Game("with my emotions"), status=discord.Status.do_not_disturb)

    try:
        synced = await bot.tree.sync()  # Syncs slash commands globally
        print(f"Synced {len(synced)} commands.")

    except Exception as e:
        print(f"Error syncing commands: {e}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())
