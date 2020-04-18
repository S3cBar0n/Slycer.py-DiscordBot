import discord
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get


# This references the client we created within our bot.py and passes it into the cog
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Commands -------------------
    # Join command for the Music Bot
    @commands.command(pass_context=True, aliases=["j"])
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"DJ Baron Bot has connected to {channel}.\n")
        await ctx.send(f"DJ Baron Bot has joined {channel}.")

    # Leave command for the Music Bot
    @commands.command(pass_context=True, aliases=["l"])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"DJ Baron Bot has left {channel}.")
            await ctx.send(f"DJ Baron Bot has left {channel}.")
        else:
            print(f"DJ Baron Bot could not leave {channel}.")
            await ctx.send(f"Are you sure I am in {channel}?")

    # Play command for the Music Bot
    @commands.command(pass_context=True, aliases=["p"])
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Previous song has been removed.")
        except PermissionError:
            print("Previous song failed to delete. (Being Played)")
            await ctx.send("ERROR: Music is currently being played.")

        await ctx.send("Getting Music Ready!")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        try:
            if voice and voice.is_playing():
                print("Replacing current song")
                voice.stop()
                await ctx.send("Stopping current song, playing next.")
        except:
            print("Replacing the currently playing song failed.")
            await ctx.send("ERROR: Could not replace the current song.")

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",

            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.08

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname}")
        print("Playing\n")

    # Pause command
    @commands.command(pass_context=True, aliases=["pa", "pau"])
    async def pause(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Music has been paused.")
        else:
            print("Music failed to pause.")
            await ctx.send("Music is not being currently played.")

    # Resume Command
    @commands.command(pass_context=True, aliases=["r"])
    async def resume(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Music has been resumed")
            voice.resume()
            await ctx.send("Music has resumed.")
        else:
            print("Music not paused.")
            await ctx.send("Music is not currently paused.")

    # Stop Command
    @commands.command(pass_context=True, aliases=["s"])
    async def stop(self, ctx):

        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music stopped.")
            voice.stop()
            await ctx.send("Music has been stopped.")
        else:
            print("No Music playing - Music failed to stop.")
            await ctx.send("No music currently playing, failed to stop.")

    # Queue



# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Music(client))
