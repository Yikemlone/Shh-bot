
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


# Define the bot
bot = commands.Bot(command_prefix="!", intents=intents,
                      help_command=CustomHelpCommand(), 
                      voice_client=discord.VoiceClient)


async def load_extensions():
    """Loads all the cogs in the cogs folder."""
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
           await bot.load_extension(f"cogs.{filename[:-3]}")


def is_guild_owner(interaction : discord.Interaction):
    """Decorator to check if the command user is the server owner."""
    if interaction.user.id != interaction.guild.owner_id: return 
    return True


def check_user_role(interaction : discord.Interaction, role_name: str):
    """Checks if the user has the role."""
    for role in interaction.user.roles:
        if role.name == role_name:
            return True
    return False


@bot.event
async def on_message(message):
    """ This function will be called whenever a message is sent in the server."""
    if message.author.bot: return
    await bot.process_commands(message)


@bot.tree.command(name="load", description="Loads the COGS into the bot") 
async def load(interaction : discord.Interaction, extension : str):

    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.")
        return
    
    await bot.load_extension(f"cogs.{extension}")
    await interaction.response.send_message("Loaded cog.")


@bot.tree.command(name="unload", description="Unloads the COGS from the bot") 
async def unload(interaction : discord.Interaction, extension : str):

    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.")
        return

    await bot.unload_extension(f"cogs.{extension}")
    await interaction.response.send_message("Unloaded cog.")


@bot.tree.command(name="reload", description="Reloads the COGS into the bot") 
async def reload(interaction : discord.Interaction, extension : str):
   
    if not is_guild_owner(interaction):
        await interaction.response.send_message("You are not the server owner.")
        return

    await bot.unload_extension(f"cogs.{extension}")
    await bot.load_extension(f"cogs.{extension}")
    await interaction.response.send_message("Reloaded cog.")


@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(activity=discord.Game("with my emotions"), status=discord.Status.do_not_disturb)

    try:
        synced = await bot.tree.sync()  # Syncs slash commands globally
        print(f"Synced {len(synced)} commands.")

    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name="ez", description="This is for a monkey.")
async def _ez(interaction: discord.Interaction):
    # TODO: Check if this is Fylik
    await interaction.response.send_message("ggez no re, bot :)")
    


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())
