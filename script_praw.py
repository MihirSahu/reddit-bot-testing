import praw
import json

client_id = ''
secret_key = ''
username = '' 
password = ''
user_agent = ''

reddit = praw.Reddit(client_id=client_id, client_secret=secret_key, password=password, username=username, user_agent=user_agent)

sub = '' 
title = ''
text = ''

subreddit = reddit.subreddit(sub)
subreddit.submit(title, selftext=text)