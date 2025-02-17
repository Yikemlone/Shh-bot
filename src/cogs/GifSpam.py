import random
import discord
from discord.ext import commands
from util.giphyconnection import GiphyConnection
from util.logger import logging

logger = logging.getLogger("shh-bot")

class GifSpam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.gif_on = False


    @commands.Cog.listener()
    async def on_message(self, message):
        """Will check if the bot should post gifs."""
        if message.author.bot:
            return

        if self.gif_on:
            await self.post_gif(message)


    @discord.app_commands.command(name="gif", description="This toggles the bot on and off from posting gifs.")
    async def gif(self, interaction: discord.Interaction):
        """Toggles the bot on and off from posting gifs."""
        
        if not self.bot.check_user_role(interaction, "Admin"):
            await interaction.response.send_message("❌ You do not have the Admin role!", ephemeral=True)
            return

        self.gif_on = not self.gif_on


    async def post_gif(self, message):
        """Will post a gif in the server"""
        ctx = await self.bot.get_context(message)
        word = message.content
        gif_data = GiphyConnection.get_data(word)

        if len(gif_data) == 0:
            return

        await ctx.send(random.choice(gif_data)["url"])


async def setup(bot):
    await bot.add_cog(GifSpam(bot))