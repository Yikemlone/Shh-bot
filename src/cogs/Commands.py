import asyncio
import random
import os
import discord
from requests import get
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.file = open(os.path.join("src/text_files", "beemovie.txt"), newline=None)


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
        # Check the user if they have the role
       
        
        for i in self.file:
            if i == "\n":
                continue

            self.file.readline()
            await asyncio.sleep(1)
            await ctx.send(i)


    @commands.command(aliases=["stopSpam"])
    async def stop_spam(self, ctx):
        self.file.close()


    @commands.command(aliases=["type"])
    async def _type(self, ctx):
        messages = {
            "avatar": ctx.author.avatar_url,
            "message": "This you?",
            "GIF": "https://tenor.com/view/kermit-the-frog-drive-driving-gif-12873213"
        }

        for message in messages:
            await ctx.trigger_typing()
            await asyncio.sleep(1.5)
            await ctx.send(messages[message])


    # @commands.command(aliases=["IP", "ip"])
    # async def _get_IP(self, ctx):
    #     ip = get('https://api.ipify.org').text
    #     await ctx.send(f"The server IP is: {ip}")

    @discord.app_commands.command(name="js", description="Says hello!")
    async def js(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


async def setup(client):
    await client.add_cog(BasicCommands(client))
