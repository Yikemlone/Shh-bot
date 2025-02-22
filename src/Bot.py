
import discord
import os
import asyncio
from discord.ext import commands
import discord.ext
import discord.ext.commands
from util.logger import logging, SHH_BOT
from util.util import is_guild_owner
from util.exceptionhandler import on_command_errors

logger = logging.getLogger(SHH_BOT)

# Define the intents, this is required for the bot to work
intents = discord.Intents.all()
intents.message_content = True

# Define the bot
bot = commands.Bot(command_prefix="!", intents=intents, voice_client=discord.VoiceClient)


async def load_extensions():
    """Loads all the cogs in the cogs folder."""
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
           await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.tree.command(name="list_extentions", description="Display a list of the COGS the bot has.") 
async def list_extensions(interaction : discord.Interaction):
    """Lists all the cogs in the cogs folder."""
    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.", ephemeral=True)
        return

    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            print(filename)


@bot.event
async def on_message(message):
    """ This function will be called whenever a message is sent in the server."""
    if message.author.bot: return
    await bot.process_commands(message)


@bot.tree.command(name="load", description="Loads the COGS into the bot") 
async def load(interaction : discord.Interaction, extension : str):

    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.", ephemeral=True)
        return
    
    await bot.load_extension(f"cogs.{extension}")
    await interaction.response.send_message("Loaded cog.")


@bot.tree.command(name="unload", description="Unloads the COGS from the bot") 
async def unload(interaction : discord.Interaction, extension : str):

    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.", ephemeral=True)
        return

    await bot.unload_extension(f"cogs.{extension}")
    await interaction.response.send_message("Unloaded cog.")


@bot.tree.command(name="reload", description="Reloads the COGS into the bot") 
async def reload(interaction : discord.Interaction, extension : str):
   
    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.", ephemeral=True)
        return

    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")
    await interaction.response.send_message("Reloaded cog.")


@bot.event
async def on_ready():
    logger.info(f"Bot is ready. Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game("fiddles"), status=discord.Status.do_not_disturb)
    bot.tree.on_error = on_command_errors

    try:
        synced = await bot.tree.sync()  # Syncs slash commands globally
        logger.info(f"Synced {len(synced)} commands.")

    except Exception as e:
        logger.error(f"Error syncing commands: {e}")


async def main():
    await load_extensions()
    await bot.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())
