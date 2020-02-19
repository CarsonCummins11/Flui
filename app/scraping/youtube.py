from app.scraping.authentication.auth import auth_data
import requests
import re
from bs4 import BeautifulSoup

#
# FILE IS NOT TESTED
#

class YoutubeBot:
	def __init__(self):
		self.youtube_404 = requests.get("https://www.youtube.com/user/test404error")
		self.youtuberooturl = "https://www.youtube.com/"
		self.youtubeuserurl = "https://www.youtube.com/user/"
		self.youtubechannelid = "https://www.youtube.com/channel/"
		self.youtubesearchurl = "https://www.youtube.com/results?search_query="
		self.soup = BeautifulSoup(self.youtube_404, 'html.parser')
		
	#tests if a youtuber exists by comparing it to youtube's 404 page
	def exists(self, youtuber):
		url = self.youtubeuserurl + youtuber
		return (requests.get(url) != self.youtube_404)
	
	#given a username, create and return an json of the user's basic info with some calculated stats
	def get_user_by_name(self, youtuber):
		if(self.exists(youtuber)):
			page = requests.get(youtubeuserurl + youtuber)
			self.soup = BeautifulSoup(page, 'html.parser')
			
			name = self.soup.find('yt-formatted-string', class_='style-scope ytd-channel-name').text
			
			page = requests.get(youtubeuserurl + youtuber + '/videos')
			self.soup = BeautifulSoup(page, 'html.parser')
			
			videos = []
			video_elms = self.soup.find_all('ytd-grid-video-renderer', class_="style-scope ytd-grid-renderer")
			
			for v in len(video_elms):
				videopage = self.youtuberooturl + self.soup.find_all('a', id="video_title")[v]['href']
				self.soup = BeautifulSoup(videopage, 'html.parser')
				likes = int(self.soup.find('yt-formatted-string', src=re.compile(r'[likes]').text)
				dislikes = int(self.soup.find('yt-formatted-string', src=re.compile(r'[dislikes]')))
				self.soup = BeautifulSoup(page, 'html.parser')
				
				videos.append({
					"author": name,
					"name": self.soup.find_all('a', id="video_title")[v],
					"link": self.soup.find_all('a', id="video_title")[v]['href'],
					"views": int(self.soup.find_all('span', class_='style-scope ytd-grid-video-renderer')[v].text.replace(' views', '')),
					"votes": likes + dislikes,
					"likes": likes,
					"dislikes": dislikes
				})
			
			total_views = 0
			for v in videos:
				total_views += v['views']
			
			total_votes = 0
			for v in videos:
				total_votes += v['votes']
			
			user = {
				"username": name,
				"videos": videos,
				"total-views": total_views,
				"total-votes": total_votes,
				"engagement_ratio": total_votes / total_views
			}
			return user
			
	#make sure parsed so that ' ' is a '+'
	#a function that searches youtubers and returns an array of youtube accounts in url form
	def search_channels(self, youtuber):
		if(self.exists(youtubers)) return self.youtubeuserurl + youtuber #if there's a youtube account directly matching your query, then return it
		page = requests.get(self.youtubesearchurl + youtuber) #getting the html of the search page
		self.soup = BeautifulSoup(page, 'html.parser') #beautifulsoup object for parsing page
		channels = []
		#go through all the channel results and add the ones that have a valid url
		for channel in soup.find_all('a', class_='channel-link yt-simple-endpoint style-scope ytd-channel-renderer'):
			if(requests.get(self.youtuberooturl + channel['href']) != self.youtube_404)
				channels.append(channel['href'])
		return channels
		
	#gets the engagement score
	def get_engagement_score(self, youtuber):
		if(self.exists(youtuber))
			return self.get_user_by_name(youtuber)["engagement_ratio"]