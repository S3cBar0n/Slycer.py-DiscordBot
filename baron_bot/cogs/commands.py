import calendar
import datetime
import random
from discord.ext import commands

# ------------------- Variables -------------------
dateToday = datetime.date.today()

# Calculates how many days are in the current month
dateDaysinMonth = calendar.monthrange(dateToday.year, dateToday.month)[1]

# Variables to Calculate days until Summer Vacation
dateSchoolEnd = datetime.date(2020, 5, 15) - dateToday
dateSchoolEndStr = str(dateSchoolEnd)
dateSummer = dateSchoolEndStr.strip("0: ,")
dateSummerSentence = " until summer!"
dateSummerStart = dateSummer + dateSummerSentence

# Variables to Calculate how many days until the end of the month
dateDaysUntilMonthEnd = dateDaysinMonth - dateToday.day + 1
dateMonthEndStr = str(dateDaysUntilMonthEnd)
dateSentence = " Days until the month ends!"
dateMonthEnd = dateMonthEndStr + dateSentence


# This references the client we created within our bot.py and passes it into the cog
class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    # ------------------- Events -------------------
    # Loads bot, and lets us know when its ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as " + self.client.user.name)
        print(self.client.user.id)
        print("-------")

    # When a known command fails, throws error
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(ctx.command.name + " didn't work! Give it another try.")
        await ctx.send(error)

    # Event for monitoring command usage
    @commands.Cog.listener()
    async def on_command(self, ctx):
        print(ctx.command.name + " was invoked.")

    # Event for monitoring successful command usage
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " was invoked sucessfully.")

    # ------------------- Commands -------------------

    @commands.group(aliases=["help"])
    async def helpcmd(self, ctx):
        await ctx.send("My Current Commands: 8ball, about, addrole, dumb, nextmonth, ping, summer")

    @commands.command(aliases=['about'])
    async def aboutbot(self, ctx):
        await ctx.send("I am a clever Discord Bot that was put together as part of a project by my creator Baron!")

    @commands.command()
    async def addrole(self, ctx, arg1):
        print(arg1)

    @commands.command()
    async def dumb(self, ctx):
        await ctx.send("I am a dumb robot!")

    @commands.command()
    async def nextmonth(self, ctx):
        await ctx.send(dateMonthEnd)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def summer(self, ctx):
        await ctx.send(dateSummerStart)

    # Commands that contain a list of responses
    @commands.command()
    async def roll(self, ctx):
        responses = ["1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "6"]
        await ctx.send(random.choice(responses))

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
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Commands(client))
