# Libraries
# Imports our discord library
import discord
# Imports our library to control the host (Deleting files)
import os
import shutil
# Library for downloading YT videos
import youtube_dl
import sqlite3
# Discord libraries
from discord.ext import commands
from discord.utils import get
from os import system

# ------------------- Variables -------------------

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "SongTracker.db"))
SQL = db.cursor()


# This references the client we created within our bot.py and passes it into the cog
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Commands -------------------
    # Join command for the Music Bot
    @commands.command(pass_context=True, aliases=["j"])
    async def join(self, ctx):

        ###############################################################################################################

        SQL.execute('create table if not exists Music('
                    '"Num" integer not null primary key autoincrement, '
                    '"Server_ID" integer, '
                    '"Server_Name" text, '
                    '"Voice_ID" integer, '
                    '"Voice_Name" text, '
                    '"User_Name" text, '
                    '"Next_Queue" integer, '
                    '"Queue_Name" text, '
                    '"Song_Name" text'
                    ')')
        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        SQL.execute(f'delete from music where Server_ID ="{server_id}" and Server_Name = "{server_name}"')
        db.commit()
        user_name = str(ctx.message.author)
        queue_name = f"Queue#{server_id}"
        song_name = f"Song#{server_id}"
        channel_id = ctx.message.author.voice.channel.id
        channel_name = str(ctx.message.author.voice.channel)
        queue_num = 1
        SQL.execute(
            'insert into Music(Server_ID, Server_Name, Voice_ID, Voice_Name, User_Name, Next_Queue, Queue_Name, Song_Name) values(?,?,?,?,?,?,?,?)',
            (server_id, server_name, channel_id, channel_name, user_name, queue_num, queue_name, song_name))
        db.commit()

        ###############################################################################################################

        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is not None:
            return await voice.move_to(channel)

        await channel.connect()

        print(f"Bot has joined channel {channel}")

        await ctx.send(f"DJ Baron Bot has joined {channel}.")

    # Leave command for the Music Bot
    @commands.command(pass_context=True, aliases=["l"])
    async def leave(self, ctx):

        ###############################################################################################################

        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        channel_id = ctx.message.author.voice.channel.id
        channel_name = str(ctx.message.author.voice.channel)
        SQL.execute(f'delete from music where Server_ID = "{server_id}" and Server_Name = "{server_name}" and Voice_ID = "{channel_id}" and Voice_name = "{channel_name}"')
        db.commit()

        ###############################################################################################################

        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"DJ Baron Bot has left {channel}.")
            await ctx.send(f"DJ Baron Bot has left {channel}.")
        else:
            print(f"DJ Baron Bot could not leave {channel} or was not in the channel.")
            await ctx.send(f"Are you sure I am in {channel}?")

    # Play command for the Music Bot
    @commands.command(pass_context=True, aliases=["pl"])
    async def play(self, ctx, *url: str):

        ###############################################################################################################
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("There is a song currently playing... !stop the song or !q to add a song to the queue...")

        else:
            server_name = str(ctx.guild)
            server_id = ctx.guild.id
            channel_id = ctx.message.author.voice.channel.id
            channel_name = str(ctx.message.author.voice.channel)
            try:
                SQL.execute(
                    f'select Song_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}" and Voice_ID="{channel_id}" and Voice_Name="{channel_name}"')
                name_song = SQL.fetchone()
                SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
                name_server = SQL.fetchone()
            except:
                await ctx.send("The bot must join a voice channel to play a song: Join one and use '/join'")
                return

            ###############################################################################################################

            def check_queue():

                ###########################################################################################################

                DIR = os.path.dirname(__file__)
                db = sqlite3.connect(os.path.join(DIR, "SongTracker.db"))
                SQL = db.cursor()
                SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
                name_queue = SQL.fetchone()
                SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
                name_server = SQL.fetchone()

                ###########################################################################################################

                Queue_infile = os.path.isdir("./Queues")
                if Queue_infile is True:
                    DIR = os.path.abspath(os.path.realpath("Queues"))
                    Queue_Main = os.path.join(DIR, name_queue[0])
                    length = len(os.listdir(Queue_Main))
                    still_q = length - 1
                    try:
                        first_file = os.listdir(Queue_Main)[0]

                        song_num = first_file.split('-')[0]
                    except:
                        print("No more queued song(s)\n")
                        SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?',
                                    (server_id, server_name))
                        db.commit()
                        return

                    #######################################################################################################

                    main_location = os.path.dirname(os.path.realpath("./baron_bot"))  # Change this back to __file__
                    print(main_location)
                    print(__file__)
                    song_path = os.path.abspath(os.path.realpath(Queue_Main) + "\\" + first_file)
                    if length != 0:
                        print("Song has completed playing, playing next song\n")
                        print(f"Songs still in queue: {still_q}")
                        song_there = os.path.isfile(f"{name_song[0]}({name_server[0]}).mp3")
                        if song_there:
                            os.remove(f"{name_song[0]}({name_server[0]}).mp3")
                        shutil.move(song_path, main_location)
                        for file in os.listdir("./"):
                            if file == f"{song_num}-{name_song[0]}({name_server[0]}).mp3":
                                os.rename(file, f'{name_song[0]}({name_server[0]}).mp3')

            ###############################################################################################################

                        voice.play(discord.FFmpegPCMAudio(f'{name_song[0]}({name_server[0]}).mp3'),
                                   after=lambda e: check_queue())
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 0.07

                    else:
                        SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?',
                                    (server_id, server_name))
                        db.commit()
                        return

                else:
                    SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?',
                                (server_id, server_name))
                    db.commit()
                    print("No songs were queued before the ending of the last song\n")

            ###############################################################################################################

            song_there = os.path.isfile(f"{name_song[0]}({name_server[0]}).mp3")
            try:
                if song_there:
                    os.remove(f"{name_song[0]}({name_server[0]}).mp3")
                    SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?',
                                (server_id, server_name))
                    db.commit()
                    print("Removed old song file")
            except PermissionError:
                print("Trying to delete song file, but it's being played")
                await ctx.send("ERROR: Music playing")
                return

            ###############################################################################################################

            SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
            name_queue = SQL.fetchone()
            queue_infile = os.path.isdir("./Queues")
            if queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queues"))
                Queue_Main = os.path.join(DIR, name_queue[0])
                Queue_Main_infile = os.path.isdir(Queue_Main)
                if Queue_Main_infile is True:
                    print("Removed old queue folder")
                    shutil.rmtree(Queue_Main)

            ###############################################################################################################

            await ctx.send("Preparing the song... Please wait...")

            ###############################################################################################################

            voice = get(self.client.voice_clients, guild=ctx.guild)
            song_path = f"./{name_song[0]}({name_server[0]}).mp3"

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': False,
                'outtmpl': song_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            song_search = ' '.join(url)

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Downloading audio now\n")
                    info = ydl.extract_info(f"ytsearch1:{song_search}", download=False)
                    info_dict = info.get('entries', None)[0]
                    print(info_dict)
                    video_title = info_dict.get('title', None)
                    ydl.download([f"ytsearch1:{song_search}"])

            except:
                print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
                c_path = os.path.dirname(os.path.realpath(__file__))
                system(f"spotdl -ff {name_song[0]}({name_server[0]}) -f " + '"' + c_path + '"' + " -s " + song_search)

            voice.play(discord.FFmpegPCMAudio(f"{name_song[0]}({name_server[0]}).mp3"), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07

            await ctx.send(f"Now playing... {video_title}")

            print("Playing Song\n")

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

        ###############################################################################################################

        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        SQL.execute('update Music set Next_Queue = 1 where Server_ID = ? and Server_Name = ?', (server_id, server_name))
        db.commit()
        SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_queue = SQL.fetchone()

        ###############################################################################################################

        queue_infile = os.path.isdir("./Queues")
        if queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queues"))
            Queue_Main = os.path.join(DIR, name_queue[0])
            Queue_Main_infile = os.path.isdir(Queue_Main)
            if Queue_Main_infile is True:
                shutil.rmtree(Queue_Main)

        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Stopping Music")
            voice.stop()
            await ctx.send("Stopping Music...")
        else:
            print("No music playing... Failed to stop")
            await ctx.send("No music currently playing... Failed to stop")

    # Next Command
    @commands.command(pass_context=True, aliases=["n", "skip", "sk"])
    async def next(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Playing next song")
            voice.stop()
            await ctx.send("Playing next song")
        else:
            print("No Music playing - failed to play next song")
            await ctx.send("No music currently playing failed")

    # Volume Command
    @commands.command(pass_context=True, aliases=["v", "vol"])
    async def volume(self, ctx, volume: int):

        if ctx.voice_client is None:
            return await ctx.send("Not connected to voice channel")

        print(volume / 100)

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    # Queue
    @commands.command(pass_context=True, aliases=["q"])
    async def queue(self, ctx, *url: str):

        # Integrate this into the play command in an if statement (Aka if voice_playing is true add to the queue)

        ###############################################################################################################

        server_name = str(ctx.guild)
        server_id = ctx.guild.id
        try:
            SQL.execute(f'select Queue_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
            name_queue = SQL.fetchone()
            SQL.execute(f'select Song_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
            name_song = SQL.fetchone()
            SQL.execute(f'select Next_Queue from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
            q_num = SQL.fetchone()
        except:
            await ctx.send("The bot must join a voice channel to queue a song: Join one and use '/join'")
            return

        Queue_infile = os.path.isdir("./Queues")
        if Queue_infile is False:
            os.mkdir("Queues")
        DIR = os.path.abspath(os.path.realpath("Queues"))
        Queue_Main = os.path.join(DIR, name_queue[0])
        Queue_Main_infile = os.path.isdir(Queue_Main)
        if Queue_Main_infile is False:
            os.mkdir(Queue_Main)

        SQL.execute(f'select Server_Name from Music where Server_ID="{server_id}" and Server_Name="{server_name}"')
        name_server = SQL.fetchone()
        queue_path = os.path.abspath(
            os.path.realpath(Queue_Main) + f"\\{q_num[0]}-{name_song[0]}({name_server[0]}).mp3")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': False,
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_search = " ".join(url)

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # print("Downloading audio now\n")
                ydl.download([f"ytsearch1:{song_search}"])
                info = ydl.extract_info(f"ytsearch1:{song_search}", download=False)
                info_dict = info.get('entries', None)[0]
                video_title = info_dict.get('title', None)
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
            # q_path = os.path.abspath(os.path.realpath("Queue"))
            Q_DIR = os.path.abspath(os.path.realpath("Queues"))
            Queue_Path = os.path.join(Q_DIR, name_queue[0])
            system(
                f"spotdl -ff {q_num[0]}-{name_song[0]}({name_server[0]}) -f " + '"' + Queue_Path + '"' + " -s " + song_search)

        await ctx.send(f'Adding {video_title} to the song queue')

        SQL.execute('update Music set Next_Queue = Next_Queue + 1 where Server_ID = ? and Server_Name = ?',
                    (server_id, server_name))
        db.commit()

        print(f'Added song to the queue\n')


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Music(client))
