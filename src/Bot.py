
from calendar import c
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from util.CustomHelpCommand import CustomHelpCommand
import asyncio

# Change the working directory to the root of the project
os.chdir('F:\Programming\Python\shh-bot')
# Load the environment variables
load_dotenv(".env")

# Define the intents, this is required for the bot to work
intents = discord.Intents.all()
intents.message_content = True

# Define the client
client = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.do_not_disturb,
                      help_command=CustomHelpCommand(), voice_client=discord.VoiceClient)

async def load_extensions():
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
           await client.load_extension(f"cogs.{filename[:-3]}")


def is_server_owner(interaction: discord.Interaction):
    print(interaction.user.id)
    # if interaction.user.id == 401415617032486922:
        # return True

@client.command()
@client.checks.has_role(401415617032486922)
async def only_for_me(interaction: discord.Interaction):
    await interaction.response.send_message('I know you!', ephemeral=True)

@client.event
async def on_message(message):
    """ This function will be called whenever a message is sent in the server."""
    if message.author.bot: return
    await client.process_commands(message)


@client.command()
# @client.check(is_server_owner)
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await client.send("Loaded cog.")


@client.command()
# @client.check(is_server_owner)
async def unload(ctx, extension):
   await client.unload_extension(f"cogs.{extension}")
   await client.send("Unloaded cog.")


@client.command()
# @client.check(is_server_owner)
async def reload(ctx, extension):
   await client.unload_extension(f"cogs.{extension}")
   await client.load_extension(f"cogs.{extension}")
   await client.send("Reloaded cog.")


async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv('BOT_TOKEN'))


if __name__ == "__main__":
    asyncio.run(main())


