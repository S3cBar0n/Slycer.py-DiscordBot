import os
# import youtube_dl
from discord.ext import commands
from discord.utils import get

# ------------------- Variables -------------------
players = {}

# This references the client we created within our bot.py and passes it into the cog
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    @commands.command(pass_context=True, aliases=["j"])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"DJ Baron Bot has connected to {channel}\n")

        await ctx.send(f"Joined {channel}")








# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Music(client))
