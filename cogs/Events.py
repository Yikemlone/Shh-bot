from discord.ext import commands
import discord
import asyncio


class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.currentUser = ""
        self.timeStartedTyping = None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game("with Vyx's Titties"), status=discord.Status.do_not_disturb)
        print("Bot is ready")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        ctx = await self.client.get_context(before)
        messageAuthor = before.author.mention

        reply = f'Look who\'s trying to hide something :) ' \
                f'\n\n{messageAuthor}\'s message before: "{before.content}"' \
                f'\n{messageAuthor}\'s message after: "{after.content}"'

        await ctx.send(reply)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if self.currentUser == "":
            self.currentUser = user
            self.timeStartedTyping = when.time()
            await asyncio.sleep(30)

            return

        if user is self.currentUser:
            await channel.send(f"{user.mention} stop typing.")
        else:
            self.currentUser = ""

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f"{member.mention} has joined the server.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f"{member.mention} has left the server.")


def setup(client):
    client.add_cog(Events(client))

