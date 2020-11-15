import discord
import praw
import random
import requests
from TOKEN import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, USER_AGENT, D_JOKE_API
from aiohttp import ClientSession
from discord.ext import commands


reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     username=USERNAME,
                     password=PASSWORD,
                     user_agent=USER_AGENT)


# This references the client we created within our bot.py and passes it into the cog
class Api(commands.Cog):
    def __init__(self, client):
        self.client = client  # this allows us to access the client within our cog

    @commands.command()
    async def meme(self, ctx, subredd='memes'):
        subreddit = reddit.subreddit(subredd)
        all_submissions = []
        top = subreddit.top(limit=55)
        for submission in top:
            all_submissions.append(submission)

        random_submission = random.choice(all_submissions)
        name = random_submission.title
        url = random_submission.url

        embed = discord.Embed(title=name, color=discord.Colour.dark_purple())
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['dadjoke'])
    async def joke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/joke"

        headers = {
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
            'x-rapidapi-key': D_JOKE_API
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                r = await response.json()
                r = r["body"][0]
                print(r)
                await ctx.send(f"**{r['setup']}**\n\n||{r['punchline']}||")


# This function allows us to connect this cog to our bot
def setup(client):
    client.add_cog(Api(client))
