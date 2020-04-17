import discord
import os
from TOKEN import TOKEN
from discord.ext import commands


# Prefix for my commands
client = commands.Bot(command_prefix = "!")


# Loads our cogs library
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
# Unloads our cogs library
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")



# Searches for .py files within the cogs directory on the OS and removes .py when loaded
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)