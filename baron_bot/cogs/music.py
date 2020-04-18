import discord
import os
import shutil
import youtube_dl
from discord.ext import commands
from discord.utils import get

# ------------------- Variables -------------------
queues = {}


# This references the client we created within our bot.py and passes it into the cog
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Commands -------------------
    # Join command for the Music Bot
    @commands.command(pass_context=True, aliases=["j"])
    async def join(self, ctx):

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

        def check_queue():
            queue_infile = os.path.isdir("./cogs/Queue")
            if queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("./cogs/Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more songs in the queue.\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "/" + first_file)
                if length != 0:
                    print("Preparing next song.\n")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")

                    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.08

                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("No songs were queued before the ending of the last song.\n")

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("Previous song has been removed.")
        except PermissionError:
            print("Previous song failed to delete. (Being Played)")
            await ctx.send("ERROR: Music is currently being played.")
            return

        queue_infile = os.path.isdir("./cogs/Queue")
        try:
            Queue_folder = "./cogs/Queue"
            if queue_infile is True:
                print("Removed old Queue folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder detected")

        await ctx.send("Getting Music Ready!")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        # If a song is currently playing, stops and begins loading the requested song
        #        try:
        #            if voice and voice.is_playing():
        #                print("Replacing current song")
        #                voice.stop()
        #                await ctx.send("Stopping current song, playing next.")
        #        except:
        #            print("Replacing the currently playing song failed.")
        #            await ctx.send("ERROR: Could not replace the current song.")

        # Begins downloading the youtube file and converts to MP3
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

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
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

        queues.clear()

        if voice and voice.is_playing():
            print("Music stopped.")
            voice.stop()
            await ctx.send("Music has been stopped.")
        else:
            print("No Music playing - Music failed to stop.")
            await ctx.send("No music currently playing, failed to stop.")

    # Queue
    @commands.command(pass_context=True, aliases=["q"])
    async def queue(self, ctx, url: str):
        queue_infile = os.path.isdir("./cogs/Queue")
        if queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("/cogs/Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("./cogs/Queue") + f"/song{q_num}.%(ext)s")

        # Begins downloading the youtube file and converts to MP3
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": queue_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",

            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            await ctx.send("Adding song " + str(q_num) + " to the queue.")
            ydl.download([url])
        print("Song has been added to the queue.\n")


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Music(client))
