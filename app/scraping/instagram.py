#scraping bot for instagram

#from app.scraping.authentication.auth import auth_data
from authentication.authentication import auth_data
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError

class InstagramBot:
	#Log into instagram and init api object with auth data
	def __init__(self):
		self.api = Client(autopatch = True, authenticate = True, username = auth_data['insta_auth']['username'], password = auth_data['insta_auth']['username'])
		self.user_id = auth_data['insta_auth']["id"]
		self.potential_influencers = []
		self.indata = {}

	#calculate the engagement ratio for a specific user
	def set_engagement_ratio(self, username):
		posts = self.api.username_feed(username)
		info = self.api.username_info(username)
		
		print(info)

#testing commands, remove when finished		
print("Initializing instagram bot")
insta_bot = InstagramBot()
insta_bot.set_engagement_ratio(auth_data['insta_auth']['username'])
	