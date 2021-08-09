# go to https://www.reddit.com/prefs/apps and sign up for an app
# I made a subreddit to test this bot on r/redditapitesting1
# Secret key: xWLv0G4rlAaJFj7Q-1SMEb5R15eoLw
# Personal use script: Q_q-UXk01b5Prlr1S2UjDg

import requests
import json

# Contact reddit with data and client id/keys, receive oauth

CLIENT_ID = 'client id goes here'
SECRET_KEY = 'secret key goes here'

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': 'account username goes here',
    'password': 'account password goes here'
}

headers = {'User-Agent': 'MyAPI/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

"""
# Get content from reddit

res = requests.get('https://oauth.reddit.com/r/aww/hot', headers=headers)

# Use .keys() to get a list of keys

for post in res.json()['data']['children']:
    print(post['data']['title'])
"""