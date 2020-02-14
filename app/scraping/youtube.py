import youtube_python
from app.scraping.authentication.auth import auth_data

class YoutubeBot:
	def __init__(self):
		self.api = API(client_id='', client_secret='', api_key='', access_token='optional')