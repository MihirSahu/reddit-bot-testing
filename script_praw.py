#praw reddit api wrapper with discord bot implementation
import praw
import discord
from discord.ext import commands


client = commands.Bot(command_prefix = '!')

# Function to submit post
def submitPost(cid, key, username, password, agent, sub, title, text):

    client_id = cid
    secret_key = key
    username = username
    password = password
    user_agent = agent

    reddit = praw.Reddit(client_id=client_id, client_secret=secret_key, password=password, username=username, user_agent=user_agent)

    sub = sub
    title = title
    text = text

    subreddit = reddit.subreddit(sub)
    subreddit.submit(title, selftext=text)

# Function to inform us about the discord login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Function to detect commands
@client.event
async def on_message(message):
    if message.content[:12] == "REDDITsubmit":
        submitPost()
    
    await client.process_commands(message)

# Run discord bot with token
client.run('discord bot token')
