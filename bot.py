# import asyncio
import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(".env")

# Initializing bot with command prefix.
# Intents is needed to keep track of user statuses. i.e online/offline
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

# We are removing the default help command and adding our own.
client.remove_command("help")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "nsfw.py":
        client.load_extension(f"cogs.{filename[:-3]}")


# # # Events # # #
@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="python-bot")
    await channel.send(f"{member} has joined the server.")
    print(f"{member} has joined the server.")


@client.event
async def on_member_remove(member: discord):
    channel = discord.utils.get(member.guild.text_channels, name="python-bot")
    await channel.send(f"{member} has left the server.")
    print(f"{member} has left the server")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    ctx = await client.get_context(message)
    print(f"This is from bot.py: {message.content}")

    # This is needed to make sure the bot will detect when the user is trying a command.
    await client.process_commands(message)


@client.event
async def on_typing(channel, user, when):
    print(f"Channel {channel}")
    print(f"User {user}")
    print(f"When {when}")

    await channel.send(f"{user} shhh. Stop typing.")


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
    embed.add_field(name="3. !clear", value="Clears messages with a specified amount. Default amount is 5",
                    inline=False)
    embed.add_field(name="4. !kick", value="Kicks the specified user out of the server.", inline=False)
    embed.add_field(name="5. !ban", value="Bans the specified user out of the server.", inline=False)
    embed.add_field(name="6. !unban", value="Unbans the specified user out of the server.", inline=False)

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
async def isGifAnnoy(ctx, message):
    if "on" in message:
        await ctx.send("Gif Annoy is now on")
        return True
    elif "off" in message:
        await ctx.send("Gif Annoy is now off")
        return False
    else:
        await ctx.send("You must enter \"on\" or \"off\"")
        return False


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
async def ez(ctx):
    await ctx.send("ggez no re, bot :)")


# Bot token
client.run(os.getenv('BOT_TOKEN'))
