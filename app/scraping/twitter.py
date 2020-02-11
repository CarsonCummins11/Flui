import json
import tweepy
from app.scraping.authentication.auth import auth_data

data_file = "app/scraping/mldata/twdata.json"
likes_weight = 1
retweet_weight = 1.5

#Gets the tweets for a twitter user
#api = tweepy api
#user = string of a user's username
def get_tweets(api, user):
	statuses =  api.user_timeline(screen_name=user, count=30)
	for status in statuses:
		status = status._json
	return statuses

#class for the twitter bot
class TweepyBot():
	#init arrays and create api
    def __init__(self):
        self.twdata = {}     
        with open(data_file, 'w') as f:
            f.write(json.dumps(self.twdata))
        self.auth = tweepy.OAuthHandler(
		    auth_data['tw_auth']['api_key'],
		    auth_data['tw_auth']['api_secret']
		)
        self.auth.set_access_token(
		    auth_data['tw_auth']['access_token'],
		    auth_data['tw_auth']['access_secret']
		)
        self.api = tweepy.API(self.auth)
			
	#updates the engagement ratio
	#also dumps the text of all tweets analyzed to a json file for ML and language processing
    def set_engagement_ratio(self, influencer):
        tweets = get_tweets(self.api, influencer.tw)
        self.twdata = json.load(open(data_file))
        engagement_scores = []
        for t in tweets:
            engagement_scores.append(
				(likes_weight * t.user.favorite_count) + (retweet_weight * t.retweet_count) / t.user.followers_count
			)
            if not t.id in self.twdata.values():
                self.twdata.append({
					'id': t.id,
					'text': t.text
				})
        influencer.engagement_ratio_tw = sum(engagement_scores) / len(engagement_scores)
        with open(data_file) as f:
            json.dumps(self.twdata, f)