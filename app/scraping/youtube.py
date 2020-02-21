from app.scraping.authentication.auth import auth_data
from pytube import Pytube

#
# FILES ARE NOT TESTED
#

class YoutubeBot:
	def __init__(self):
		self.pyt = Pytube()
		
	#gets the engagement score
	def get_engagement_score(self, youtuber=None, id=None):
		return self.pyt.user(youtube=youtuber,id=id)['engagement-score']