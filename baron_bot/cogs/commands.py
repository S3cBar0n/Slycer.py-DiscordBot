# Libraries
# Imports our libraries to calculate current/future dates
import calendar
import datetime
import time
import json
import aiohttp
# Imports random so we can randomize responses
import random
# Imports our discord command library
from discord.ext import commands

# ------------------- Variables -------------------
dateToday = datetime.date.today()

# Calculates how many days are in the current month
dateDaysInMonth = calendar.monthrange(dateToday.year, dateToday.month)[1]

# Variables to Calculate days until Summer Vacation
dateSchoolEnd = datetime.date(2021, 5, 15) - dateToday
dateSchoolEndStr = str(dateSchoolEnd)
dateSummer = dateSchoolEndStr.strip("0: ,")
dateSummerSentence = " until summer!"
dateSummerStart = dateSummer + dateSummerSentence

# Variables to Calculate how many days until the end of the month
dateDaysUntilMonthEnd = dateDaysInMonth - dateToday.day + 1
dateMonthEndStr = str(dateDaysUntilMonthEnd)
dateSentence = " Days until the month ends!"
dateMonthEnd = dateMonthEndStr + dateSentence
pacing = 0

# This references the client we created within our bot.py and passes it into the cog
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog


    # ------------------- Commands -------------------
    @commands.command(aliases=["about"])
    async def aboutbot(self, ctx):
        await ctx.send(f"I am Baron Bot, I was put together as part of a project by my creator Baron!")

    @commands.command()
    async def addrole(self, arg1):  # needs to use ctx if it is going to be used.
        print(arg1)

    @commands.command()
    async def dumb(self, ctx):
        await ctx.send("I am a dumb robot!")

    @commands.command(aliases=["month"])
    async def nextmonth(self, ctx):
        await ctx.send(dateMonthEnd)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def pacer(self, ctx):
        await ctx.send("The FitnessGram Pacer Test is a multistage aerobic capacity test that progressively gets more difficult as it continues.")
        time.sleep(2)
        await ctx.send("The 20 meter pacer test will begin in 30 seconds.")
        time.sleep(1)
        await ctx.send("Line up at the start.")
        time.sleep(2)
        await ctx.send("The running speed starts slowly but gets faster each minute after you hear this signal *BEEP*")
        time.sleep(2)
        await ctx.send("A single lap should be completed every time you hear this sound: *DING*, remember to run in a straight line and run as long as possible.")
        time.sleep(2)
        await ctx.send("The second time you fail to complete a lap before the sound, your test is over.")
        time.sleep(2)
        await ctx.send("The test will begin on the word start. On your mark. Get ready!")
        time.sleep(2)
        await ctx.send("...")
        time.sleep(0.5)
        await ctx.send("...")
        time.sleep(0.5)
        await ctx.send("START! (say !pace to continue the test!)")

    @commands.command()
    async def pace(self, ctx):
        global pacing
        if pacing <= 4:
            pacing += 1
            await ctx.send(f"Lap # {pacing} completed successfully!")
        if pacing == 5:
            await ctx.send("This concludes the Pacer Gram fitness test...")
            pacing = 0

    @commands.command()
    async def summer(self, ctx):
        await ctx.send(dateSummerStart)

    # Commands that contain a list of responses
    @commands.command()
    async def roll(self, ctx):
        await ctx.send(random.randint(1, 6))

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))