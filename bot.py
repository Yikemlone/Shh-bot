import asyncio
import datetime
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
    channel = discord.utils.get(member.guild.text_channels, name="general-text")
    await channel.send(f"{member} has joined the server.")


@client.event
async def on_member_remove(member: discord):
    ctx = await client.get_context(member)
    channel = member.channel.name
    channelSend = discord.utils.get(ctx.guild.text_channels, name=channel)

    await channelSend.send(f"{member} has left the server.")


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

    print(type(before))
    print(before.content)
    print(after.content)

    await ctx.send("Look who's trying to hide something :)")


# # # Commands # # #
# @client.command(aliases=["help"])
# async def _help(ctx):
#     author = ctx.message.author
#
#     embed = discord.Embed(
#         color=discord.Color.purple()
#     )
#
#     embed.set_author(name="Commands:")
#     embed.add_field(name="1. !ping", value="Returns pong with the time it took to respond.", inline=False)
#     embed.add_field(name="2. !8ball", value="Ask a question. It will give a response to the question.", inline=False)
#     embed.add_field(name="3. !ez", value="Prints a very original tag line. :)",
#                     inline=False)
#
#     embed.add_field(name="Moderator Commands:", value=embed.Empty)
#     embed.add_field(name="1. !kick", value="Kicks the specified user out of the server.", inline=False)
#     embed.add_field(name="2. !ban", value="Bans the specified user out of the server.", inline=False)
#     embed.add_field(name="3. !unban", value="Unbans the specified user out of the server.", inline=False)
#     embed.add_field(name="4. !load", value="Loads a cog file.", inline=False)
#     embed.add_field(name="5. !unload", value="Unloads a cog file.", inline=False)
#     embed.add_field(name="6. !reload", value="Reloads a cog file.", inline=False)
#     embed.add_field(name="7. !clear", value="Clears messages with a specified amount. Default amount is 5",
#                     inline=False)
#
#     await author.send(author, embed=embed)


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
