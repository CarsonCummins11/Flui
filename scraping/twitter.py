import tweepy
from app import InfluencerProfile

'''

Api key: 3fTZMPvKj8M1ryDE1pNXRA6el

API secret key:TVet3ZZ68Qn3rtDl6IbdsmbV1pIhpuSaFHM4GCPxCZF9HS8Ffs

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

#api = tweepy.API(auth)
'''
api = None

def get_tweets(user):
    statuses =  api.get_user(user).user_timeline()
    for status in statuses:
        status = status._json
    return statuses

def get_engagement_ratio(influencer):
    tweets = get_tweets(influencer.tw)
    for t in tweets:
        
