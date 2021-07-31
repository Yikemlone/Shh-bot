import asyncio
import random
import os
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file = open(os.path.join("text_files", "beemovie.txt"), newline=None)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
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

    @commands.command()
    async def ez(self, ctx):
        await ctx.send("ggez no re, bot :)")

    @commands.command()
    @commands.has_role("Spammer")
    async def spam(self, ctx):
        for i in self.file:
            if i == "\n":
                continue

            self.file.readline()
            await asyncio.sleep(1)
            await ctx.send(i)

    @commands.command(aliases=["stopSpam"])
    async def stop_spam(self, ctx):
        self.file.close()


def setup(client):
    client.add_cog(BasicCommands(client))
