
import calendar
import datetime
import discord
import random
from discord.ext import commands



# BEGIN VARIABLES
dateToday = datetime.date.today()

# Calculates how many days are in the current month
dateDaysinMonth = calendar.monthrange(dateToday.year, dateToday.month)[1]

# Variables to Calculate days until Summer Vacation
dateSchool = datetime.date(2020, 5, 15) - datetime.date.today()
dateSchoolStr = str(dateSchool)
dateSummer = dateSchoolStr.strip("0: ,")
dateSummerSentance = " until summer!"
dateSchoolEnd = dateSummer + dateSummerSentance

# Variables to Calculate how many days until the end of the month
dateDaysUntilMonthEnd = dateDaysinMonth - dateToday.day + 1
dateMonthEndStr = str(dateDaysUntilMonthEnd)
dateSentance = " Days until the month ends!"
dateMonthEnd = dateMonthEndStr + dateSentance




class Commands(commands.Cog):
# This refrences the client we created within our bot.py and passes it into the cog
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

# Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as " + self.client.user.name)
        print(self.client.user.id)
        print("-------")


# Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command()
    async def aboutbot(self, ctx):
        await ctx.send("I am a clever Discord Bot that was put together as part of a school project by my creator @Baron!")

    @commands.command()
    async def dumb(self, ctx):
        await ctx.send("I am a dumb robot!")

    @commands.command()
    async def summer(self, ctx):
        await ctx.send(dateSchoolEnd)

    @commands.command()
    async def nextmonth(self, ctx):
        await ctx.send(dateMonthEnd)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball'])
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
               "Very doubtful.",]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")










# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))