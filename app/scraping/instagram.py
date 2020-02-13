#scraping bot for instagram

#from app.scraping.authentication.auth import auth_data
from authentication.authentication import auth_data
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
		print(info)
				
		ratios = []
		for post in posts['items']:
			ratios.append(post['like_count'] / info['follower_count']
		self.engagement_score = sum(ratios) / len(ratios)			

#testing commands, remove when finished
insta_bot = InstagramBot()
insta_bot.set_engagement_ratio(auth_data['insta_auth']['username'])