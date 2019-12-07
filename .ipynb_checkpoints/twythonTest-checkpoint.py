# Import the Twython class
from twython import Twython
import json


# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'sVems62H0RWKzzvQQRA7XudV3'
credentials['CONSUMER_SECRET'] = 'VgMggXa5lynttR4q88zbK3YVGhrc9VX0tpAiQrDL4ZUBf4AKey'
credentials['ACCESS_TOKEN'] = '1148727050628263941-GJUJIjUrQ69mjOddkxY09pHiH8dfU4'
credentials['ACCESS_SECRET'] = 'lBWT5wb2y0u3f9LzzalUDcSQsu0VwIaFu8mObbHayQPkU'

#Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)
    
#Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

#Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {'q': 'eagles',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }
import pandas as pd

# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
print(len(df))
print(df.head(5))
