import discord
from discord.ext import commands
from util.logger import logging

logger = logging.getLogger("shh-bot")
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="clear", description="Clears the chat")
    @discord.app_commands.describe(amount="The amount of messages to clear")
    # @commands.check(isServerOwner)
    async def clear(self, interaction : discord.Interaction, amount : int = 6): 
        await interaction.channel.purge(limit=amount)


    @commands.command()
    # @commands.check(isServerOwner)
    async def clearAll(self, ctx):
        await ctx.channel.purge(limit=1000000)


    @commands.command()
    # @commands.check(isServerOwner)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)


    @commands.command()
    # @commands.check(isServerOwner)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)


    @commands.command()
    # @commands.check(isServerOwner)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return


async def setup(bot):
    await bot.add_cog(Moderation(bot))
