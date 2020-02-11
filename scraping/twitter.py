import json
import copy
from requests.auth import HTTPBasicAuth
import tweepy
from app import InfluencerProfile

'''

Api key: 3fTZMPvKj8M1ryDE1pNXRA6el

API secret key:TVet3ZZ68Qn3rtDl6IbdsmbV1pIhpuSaFHM4GCPxCZF9HS8Ffs

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)

access_token ->1225240357387956225-TMEOZx7mWGHBLUNOA0EQgEwdNEOr0l
access_secret -> qsQGjoUownO2l21qx98qjEqtJt8T6IARP3p8d3lA8JaP6
#api = tweepy.API(auth)
'''
api = None

likes_weight = 1
retweet_weight = 1.5

def get_tweets(api, user):
	statuses =  api.get_user(user).user_timeline()
	for status in statuses:
		status = status._json
	return statuses

#class for the twitter bot
class TweepyBot():
	#init arrays and create api
	def __init__(self):
		self.engagement_scores = []
		self.big_data_txt = {}
	
	#updates the engagement ratio
	def set_engagement_ratio(self, influencer):
		tweets = get_tweets(influencer.tw)
		for t in tweets:
			engagement_scores.append(
				(likes * t.user.favorite_count) + (retweet_weight * t.retweet_count) / t.user.followers_count
			)
			if not t.id in big_data_txt.values():
				big_data_txt.append({
					'id': t.id,
					'text': t.text
				})
		influencer.engagement_ratio_tw = sum(engagement_scores) / len(engagement_scores)
		
	#returns an array of {"id": t.id, "text": t.text} for Carson's ML
	def get_big_text_data(self):
		duplication = copy.copy(big_data_txt) #does this code suck, probably
		self.big_data_txt.clear()
		return duplication
	
#tb = TweepyBot() #used for testing