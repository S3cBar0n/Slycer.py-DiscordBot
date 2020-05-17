# Libraries
# Library for OS file control
import os
# Imports file that contains our bots token
from TOKEN import bot_token
# Imports our discord command library
from discord.ext import commands

# Prefix for my commands
client = commands.Bot(command_prefix="!", help_command=None)


# Loads our cogs library
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


# Unloads our cogs library
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


# Searches for .py files within the cogs directory on the OS and removes .py so it can be loaded
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(bot_token)
