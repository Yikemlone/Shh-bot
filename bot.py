import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

# Securing bot token
load_dotenv(".env")

# Initializing bot with command prefix.
client = commands.Bot(command_prefix="!")


# Events
@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_member_join(member):
    await member.send(f"{member} has joined the server.")
    print(f"{member} has joined the server.")


@client.event
async def on_member_remove(member):
    await member.send(f"{member} has joined the server.")
    print(f"{member} has left the server")


@client.event
async def on_message(message):
    print(message.content)
    await client.process_commands(message)


# Commands
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

# Bot token
client.run(os.getenv('BOT_TOKEN'))
