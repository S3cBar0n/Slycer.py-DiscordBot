import youtube_dl
from discord.ext import commands

# ------------------- Variables -------------------
players = {}

# This references the client we created within our bot.py and passes it into the cog
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        server = self.ctx.message.server
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()











# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Music(client))
