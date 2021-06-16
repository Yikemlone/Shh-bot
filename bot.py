# import asyncio
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

# VCBot = discord.VoiceClient

client = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.do_not_disturb)

# We are removing the default help command and adding our own.
client.remove_command("help")

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

    # channel = discord.utils.get(member.guild.text_channels, name="general-text")
    await channelSend.send(f"{member} has left the server.")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    ctx = await client.get_context(message)

    # for emoji in client.emojis:
    #     await ctx.send(emoji)

    # This is needed to make sure the bot will detect when the user is trying a command.
    await client.process_commands(message)


@client.event
async def on_typing(channel, user, when):

    beforeTime = when.time()
    # await asyncio.sleep(20)
    timeAfter = datetime.datetime.now().time()

    # if timeAfter > beforeTime:
    #     await channel.send(f"{user} what are you typing? Stop it.")


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
@client.command(aliases=["help"])
async def _help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        color=discord.Color.purple()
    )

    embed.set_author(name="Commands:")
    embed.add_field(name="1. !ping", value="Returns pong with the time it took to respond.", inline=False)
    embed.add_field(name="2. !8ball", value="Ask a question. It will give a response to the question.", inline=False)
    embed.add_field(name="3. !ez", value="Prints a very original tag line. :)",
                    inline=False)

    embed.add_field(name="Moderator Commands:", value=embed.Empty)
    embed.add_field(name="1. !kick", value="Kicks the specified user out of the server.", inline=False)
    embed.add_field(name="2. !ban", value="Bans the specified user out of the server.", inline=False)
    embed.add_field(name="3. !unban", value="Unbans the specified user out of the server.", inline=False)
    embed.add_field(name="4. !load", value="Loads a cog file.", inline=False)
    embed.add_field(name="5. !unload", value="Unloads a cog file.", inline=False)
    embed.add_field(name="6. !reload", value="Reloads a cog file.", inline=False)
    embed.add_field(name="7. !clear", value="Clears messages with a specified amount. Default amount is 5",
                    inline=False)

    await author.send(author, embed=embed)


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


# Setting a default amount of messages to clear in the parameters
@client.command()
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)


@client.command()
async def clearAll(ctx):
    await ctx.channel.purge(limit=1000000)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


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


@client.command()
async def spam(ctx):
    f = open(os.path.join("files/beemovie.txt"), newline=None)

    for i in f:
        if i == "\n":
            continue

        f.readline()
        await asyncio.sleep(1)
        await ctx.send(i)


@client.command()
async def ez(ctx):
    await ctx.send("ggez no re, bot :)")


@client.command()
async def join(ctx):

    vc = discord.utils.get(ctx.guild.voice_channels, name="General")

    await vc.connect()

# Bot token
client.run(os.getenv('BOT_TOKEN'))
