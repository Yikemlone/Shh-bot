from discord.ext import commands
import discord
import asyncio


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")
        await self.client.change_presence(activity=discord.Game("with Connor's Titties"),
                                          status=discord.Status.do_not_disturb)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        ctx = await self.client.get_context(before)
        message_author = before.author.mention

        reply = f'Look who\'s trying to hide something :) ' \
                f'\n\n{message_author}\'s message before: "{before.content}"' \
                f'\n{message_author}\'s message after: "{after.content}"'

        await ctx.send(reply)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ When a new member joins, posts a message in chat"""
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f"{member.mention} has joined the server.")


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """ When a member leavs, posts a message in chat"""
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f"{member.mention} has left the server.")


async def setup(client):
    await client.add_cog(Events(client))