import tweepy
#Twitter API credentials
auth = tweepy.OAuthHandler('', '')
api = tweepy.API(auth)
# Create our query
query = {'q': 'eagles golden',
        'lang': 'en',
        }

#Run initial Search
i = 0
dTweets = {}
for status in api.search(**query, tweet_mode='extended'):
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'id': []}
    dict_['user'].append(status.user.screen_name)
    dict_['date'].append(status.created_at)
    dict_['text'].append(status.full_text)
    dict_['favorite_count'].append(status.favorite_count)
    dict_['id'].append(status.id)
    dTweets[i] = dict_
    i += 1

#Run 10 more searches using the same query 
for round in range(0, 10):    
    lIDs = []
    for key in dTweets:
        lIDs.append(dTweets[key]['id'][0])
    query['max_id'] = min(lIDs) - 1
    i = len(dTweets)
    for status in api.search(**query, tweet_mode='extended'):
        dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'id': []}
        dict_['user'].append(status.user.screen_name)
        dict_['date'].append(status.created_at)
        dict_['text'].append(status.full_text)
        print(status.full_text)
        dict_['favorite_count'].append(status.favorite_count)
        dict_['id'].append(status.id)
        dTweets[i] = dict_
        i += 1
        
# Save Each tweet in separate file
sDirectory = 'tweets/'
sFilename = ''
for entry in dTweets:
    sFilename = sDirectory + str(dTweets[entry]['id']) + '-0'
    fFile = file1 = open(sFilename,"a")
    sText = str(dTweets[entry]['text'])
    sText = sText[2:(len(sText)-2)]
    fFile.write(sTe
                xt)
    fFile.close
