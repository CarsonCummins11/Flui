#scraping bot for instagram

#uncomment this when running with python3 -m flask run(running the whole app)
#from app.scraping.authentication.auth import auth_data
from authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError

class InstagramBot:
	#Log into instagram and init api object with auth data
	def __init__(self):
		self.api = Client(autopatch = True, authenticate = True, username = auth_data['insta_auth']['username'], password = auth_data['insta_auth']['password'])
		self.user_id = auth_data['insta_auth']["id"]
		self.potential_influencers = []
		self.indata = {}
		self.engagement_score = 0

	#calculate the engagement ratio for a specific user
	def set_engagement_ratio(self, username):
		posts = self.api.username_feed(username)
		info = self.api.username_info(username)
		
		ratios = []
		for post in posts['items']:
			ratios.append(post['like_count'] / info['follower_count']
		self.engagement_score = sum(ratios) / len(ratios)

#testing commands, remove when finished
insta_bot = InstagramBot()
insta_bot.set_engagement_ratio(auth_data['insta_auth']['username'])