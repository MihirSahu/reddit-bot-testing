#praw reddit api wrapper with discord bot implementation
import praw
import discord
from discord.ext import commands
import ast
import requests
import time
from multiprocessing import Process
import urllib.request
import random


client = commands.Bot(command_prefix = '!')

client_id = ''
secret_key = ''
username = ''
password = ''
user_agent = ''

autoPostFlag = False

# Function to submit custom post
def submitPost(cid, key, username, password, agent, info):

    sub = info['sub']
    title = info['title']
    text = info['text']

    reddit = praw.Reddit(client_id=cid, client_secret=key, username=username, password=password,  user_agent=agent)

    subreddit = reddit.subreddit(sub)
    subreddit.submit(title, selftext=text)

# Function to submit custom pictures
def submitPics(cid, key, username, password, agent, info):

    sub = info['sub']
    title = info['title']
    link = info['link']

    # Create random string
    randomString = output_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))

    # Pretend like we're a normal user and not a bot
    opener=urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    urllib.request.urlretrieve(link, filename="pictures/{rand}.jpg".format(randomString))

    reddit = praw.Reddit(client_id=cid, client_secret=key, username=username, password=password,  user_agent=agent)

    subreddit = reddit.subreddit(sub)
    subreddit.submit_image(title, image_path='pictures/{rand}.jpg'.format(randomString))

# Function to autosubmit posts at certain time
def autoPost(cid, key, username, password, agent, flag, info):

    sub = info['sub']
    title = info['title']
    text = info['text']
    day = int(info['day'])
    hour = int(info['hour'])
    minute = int(info['minute'])


    while (flag == True):
        req = requests.get('https://timeapi.io/api/Time/current/zone?timeZone=US/Central').json()

        if (minute == req['minute']):
            reddit = praw.Reddit(client_id=cid, client_secret=key, username=username, password=password,  user_agent=agent)

            subreddit = reddit.subreddit(sub)
            subreddit.submit(title, selftext=text)
            time.sleep(60)

# Function to inform us about the discord login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Function to detect commands
@client.event
async def on_message(message):
    if message.content[:12] == "redditsubmit":
        await message.channel.send('Recieved but no action')

    elif message.content[:18] == "customredditsubmit":

        info = ast.literal_eval(message.content[19:])
        submitPost(client_id, secret_key, username, password, user_agent, info)
        await message.channel.send('custom post submitted')

    elif message.content[:22] == "customredditsubmitpics":

        info = ast.literal_eval(message.content[23:])
        submitPics(client_id, secret_key, username, password, user_agent, info)
        await message.channel.send('custom pic submitted')

    elif message.content[:19] == "autoredditsubmit on":
        
        autoPostFlag = True
        info = ast.literal_eval(message.content[20:])
        p = Process(target=autoPost, args=(client_id, secret_key, username, password, user_agent, autoPostFlag, info))
        p.start()
        await message.channel.send('autosubmit turned on')
    
    elif message.content[:20] == "autoredditsubmit off":
        
        autoPostFlag = False
        await message.channel.send('autosubmit turned off')

    elif message.content[:19] == '?customredditsubmit':
        await message.channel.send('To submit a custom reddit post enter \'customredditsubmit {\'sub\': \'sub name\', \'title\': \'title of post\', \'text\': \'text in post\'}\'')

    elif message.content[:19] == '?customredditsubmitpics':
        await message.channel.send('To submit a custom reddit post enter \'customredditsubmit {\'sub\': \'sub name\', \'title\': \'title of post\', \'link\': \'link here\'}\'')
    
    elif message.content[:17] == '?autoredditsubmit':
        await message.channel.send('To auto submit a custom reddit post enter in a given time \'autoredditsubmit on {\'sub\': \'sub name\', \'title\': \'title of post\', \'text\': \'text in post\', \'day\': \'day to post\', \'hour\': \'military time\', \'minute\': \'minute\'}\'')
    
    await client.process_commands(message)

# Run discord bot with token
client.run('')