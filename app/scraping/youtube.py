#from app.scraping.authentication.auth import auth_data
#from pytube import Pytube
import requests
import youtube_dl
import re
#
# FILES ARE NOT TESTED
#

class YoutubeBot:
	def __init__(self):
		#self.pyt = Pytube()
		print('made')
		
	#gets the engagement score
	def get_engagement_score(self, youtuber=None, id=None):
		return self.pyt.user(youtube=youtuber,id=id)['engagement-score']
	def get_captions(self,url):
		ydl = youtube_dl.YoutubeDL({'writesubtitles': True, 'allsubtitles': True, 'writeautomaticsub': True})
		res = ydl.extract_info(url, download=False)
		if res['requested_subtitles'] and res['requested_subtitles']['en']:
			print('Grabbing vtt file from ' + res['requested_subtitles']['en']['url'])
			response = requests.get(res['requested_subtitles']['en']['url'], stream=True)
			new = re.sub(r'\d{2}\W\d{2}\W\d{2}\W\d{3}\s\W{3}\s\d{2}\W\d{2}\W\d{2}\W\d{3}','',response.text)
			return new
		else:
			print('Youtube Video does not have any english captions')
			return ''