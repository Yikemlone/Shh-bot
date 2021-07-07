import asyncio
import datetime
from pprint import pprint

import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(".env")

# Initializing bot with command prefix.
# Intents is needed to keep track of user statuses. i.e online/offline
intents = discord.Intents.all()


class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            if cog is None:
                continue
            await self.get_destination().send(f"{cog.qualified_name}: {[command.name for command in mapping[cog]]}")

    async def send_cog_help(self, cog):
        await self.get_destination().send(f"{cog.qualified_name}: {[command.name for command in cog.get_commands()]}")

    async def send_group_help(self, group):
        await self.get_destination().send(f"{group.name}: {[command.name for index, command in enumerate(group.commands)]}")

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)


client = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.do_not_disturb,
                      help_command=CustomHelpCommand())


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "nsfw.py":
        client.load_extension(f"cogs.{filename[:-3]}")


# # # Events # # #
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("with Vyx's Titties"), status=discord.Status.do_not_disturb)
    print("Bot is ready")


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    await channel.send(f"{member.mention} has joined the server.")


@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    await channel.send(f"{member.mention} has left the server.")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    # This is needed to make sure the bot will detect when the user is trying a command.
    await client.process_commands(message)


@client.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    ctx = await client.get_context(before)
    messageAuthor = before.author.mention

    reply = f'Look who\'s trying to hide something :) ' \
            f'\n\n{messageAuthor}\'s message before: "{before.content}"'\
            f'\n{messageAuthor}\'s message after: "{after.content}"'

    await ctx.send(reply)


# # # Commands # # #
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


# Creating an alias for this command
@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is Certain.",
                 "It is decidedly so."
                 "Without a doubt.", "Yes definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]

    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


file = open(os.path.join("files/beemovie.txt"), newline=None)


@client.command()
@commands.has_role("Spammer")
async def spam(ctx):
    for i in file:
        if i == "\n":
            continue

        file.readline()
        await asyncio.sleep(1)
        await ctx.send(i)


@client.command()
async def stopSpam(ctx):
    file.close()


@client.command()
async def ez(ctx):
    await ctx.send("ggez no re, bot :)")

# Bot token
client.run(os.getenv('BOT_TOKEN'))
