import discord
from discord.ext import commands


def isServerOwner(ctx):
    if ctx.author.id == 401415617032486922:
        return True


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Setting a default amount of messages to clear in the parameters
    @commands.command()
    @commands.check(isServerOwner)
    async def clear(self, ctx, amount=6):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.check(isServerOwner)
    async def clearAll(self, ctx):
        await ctx.channel.purge(limit=1000000)

    @commands.command()
    @commands.check(isServerOwner)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    @commands.check(isServerOwner)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    @commands.check(isServerOwner)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return


def setup(client):
    client.add_cog(Moderation(client))
