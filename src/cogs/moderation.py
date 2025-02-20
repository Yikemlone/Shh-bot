import discord
from discord.ext import commands
from util.logger import logging, SHH_BOT

logger = logging.getLogger(SHH_BOT)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="clear", description="Clears the chat")
    @discord.app_commands.describe(amount="The amount of messages to clear")
    @discord.app_commands.guild_only()
    async def clear(self, interaction : discord.Interaction, amount : int = 6): 
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"✅ Cleared {amount} messages.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
