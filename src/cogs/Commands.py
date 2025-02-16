import asyncio
import random
import os
import discord
from requests import get
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = open(os.path.join("src/text_files", "beemovie.txt"), newline=None)


    @discord.app_commands.command(name="ping", description="Check the latency of the bot.")
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")


    @discord.app_commands.command(name="8ball", description="Ask a question and the bot will answer.")
    @discord.app_commands.describe(question="The question you want to ask the bot.")
    async def _8ball(self, interaction: discord.Interaction, question: str):
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

        await interaction.response.send_message(f"Question: {question}\nAnswer: {random.choice(responses)}")


    # @discord.app_commands.command(name="ez", description="This is for a monkey.")
    # async def _ez(self, interaction: discord.Interaction):
    #     # TODO: Check if this is Fylik
    #     print(interaction.author)
    #     await interaction.response.send_message("ggez no re, bot :)")


    @discord.app_commands.command(name="spam", description="This will spam the chat with the bee movie script.")
    async def _spam(self, interaction: discord.Interaction):
        userHasRole = self.bot.check_user_role(interaction, "Spammer")

        if not userHasRole:
            await interaction.response.send_message("❌ You do not have the Spammer role!", ephemeral=True)
            
        for i in self.file:
            if i == "\n":
                continue

            self.file.readline()
            await asyncio.sleep(1)
            await interaction.response.send_message(i)


    @discord.app_commands.command(name="stopspam", description="This will stop the spam.")
    async def _stop_spam(self, ctx):
        self.file.close()


    @discord.app_commands.command(name="type", description="This is a test typing command.")
    async def _type(self, interaction: discord.Interaction):

        messages = {
            "avatar": interaction.author.avatar_url,
            "message": "This you?",
            "GIF": "https://tenor.com/view/kermit-the-frog-drive-driving-gif-12873213"
        }

        for message in messages:
            await interaction.trigger_typing()
            await asyncio.sleep(1.5)
            await interaction.response.send_message(messages[message])


    # @commands.command(aliases=["IP", "ip"])
    # async def _get_IP(self, ctx):
    #     ip = get('https://api.ipify.org').text
    #     await ctx.send(f"The server IP is: {ip}")


async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
