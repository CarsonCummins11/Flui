import json
import tweepy
from TwitterSearch import *
from app.scraping.authentication.auth import auth_data

data_file = "app/scraping/mldata/twdata.json"
likes_weight = 1
retweet_weight = 1.5
follower_threshold = 1

#Gets the tweets for a twitter user
#api = tweepy api
#user = string of a user's username
def get_tweets(api, user):
	statuses =  api.user_timeline(screen_name=user, count=30)
	for status in statuses:
		status = status._json
	return statuses

#class for the twitter bot
class TweepyBot:
	#init arrays and create api
    def __init__(self):
        self.potential_influencers = []
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
        self.tso = TwitterSearchOrder()
        self.tso.set_language("en")
        self.tso.set_include_entities(False)
        self.ts = TwitterSearch(
            consumer_key=auth_data['tw_auth']['api_key'],
            consumer_secret=auth_data['tw_auth']['api_secret'],
            access_token=auth_data['tw_auth']['access_token'],
            access_token_secret=auth_data['tw_auth']['access_secret']
        )
			
	#updates the engagement ratio
	#also dumps the text of all tweets analyzed to a json file for ML and language processing
    def set_engagement_ratio(self, influencer):
        tweets = get_tweets(self.api, influencer.tw)
        self.twdata = json.load(open(data_file))
        count=0
        engagement_scores = []
        for t in tweets:
            engagement_scores.append(
				(likes_weight * t.user.favorite_count) + (retweet_weight * t.retweet_count) / t.user.followers_count
			)
            if not t.id in self.twdata.values():
                self.twdata[count] = {
					'id': t.id,
					'text': t.text,
                    'engagement_score': engagement_scores[-1]
				}
                count+=1
        influencer.engagement_ratio_tw = sum(engagement_scores) / len(engagement_scores)
        #{k: v for k, v in sorted(self.twdata.items(), key=lambda item: item[1])} #sorts by engagement
        with open(data_file, 'w') as f:
            f.write(json.dumps(self.twdata))
        self.twdata.clear() #for ram

    #searches tweets with a given str array of keywords 
    #also dumps tweet data to mldata/twdata.json
    def search(self, keywords):
        self.tso.set_keywords(keywords)
        self.twdata = json.load(open(data_file))
        count=0
        for tweet in self.ts.search_tweets_iterable(self.tso):
            if(tweet['user']['followers_count'] > follower_threshold):
                self.potential_influencers.append(tweet['user']['screen_name'])
                if not tweet['id'] in self.twdata.values():
                    self.twdata[count] = {
                        'id': tweet['id'],
                        'text': tweet['text'],
                        'engagement_score': ((likes_weight * tweet['favorite_count']) + (retweet_weight * tweet['retweet_count']) / tweet['user']['followers_count'])
                    }
                    count+=1
        #{k: v for k, v in sorted(self.twdata.items(), key=lambda item: item[1])} #sorts by engagement
        with open(data_file, 'w') as f:
            f.write(json.dumps(self.twdata))
        self.twdata.clear() #for ram