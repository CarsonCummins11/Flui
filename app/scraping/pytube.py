#pytube object for scraping youtube
from bs4 import BeautifulSoup
import requests
import re

#returns true if the page of the url is one of youtube's 2 404 pages
def is404(url):
	page = requests.get(url).text #sets the page
	soup = BeautifulSoup(page, 'html.parser')
	error_404 = soup.find(id="error-page-hh-illustration") #broad 404 error
	error_404_channel = soup.find(class_="channel-empty-message banner-message") #channel 404 error
	if error_404 != None or error_404_channel != None:
		return False;
	return True;

#class that does all the scraping
class Pytube:
	#set the youtube urls
	def __init__(self):
		self.youtuberoot = "https://youtube.com/"
		self.youtubeuser = self.youtuberoot + "user/"
		self.youtubeid = self.youtuberoot + "channel/"
		self.youtubesearchurl = "https://www.youtube.com/results?search_query="
	
	#gets a user from a username or id
	def user(self, username=None, id=None):
		root = None #root channel bs4 object
		root_url = None #url of the channel
		
		user_obj = { #object of the yt user to be returned
			"username": username,
			"channel-name": None,
			"subscribers": None,
			"videos": None,
			"total-views": None,
			"total-votes": None,
			"engagement-ratio": None
		}
		
		#make sure the channel exists
		u_exists = is404(self.youtubeuser + str(username))
		id_exists = is404(self.youtubeid + str(id))
		
		#set the root and root_url depending on if the username or id isn't None
		if u_exists:
			root = requests.get(self.youtubeuser + username).text
			root_url = self.youtubeuser + username + "/"
		elif id_exists:
			root = requests.get(self.youtubeid + id).text
			root_url = self.youtubeid + id + "/"
		
		#if this is None by this point, the channel isn't real
		if root == None:
			return "Unable to find user or id"
		
		#creates the bs4 object for the video page
		videos = requests.get(root_url + "videos/").text

		#set's the two pages needed for scraping user info
		soup_root = BeautifulSoup(root, 'html.parser')
		soup_videos = BeautifulSoup(videos, 'html.parser')
		
		#setting the channel name, subscribers and username
		user_obj['channel-name'] = soup_root.find('a', class_="spf-link branded-page-header-title-link yt-uix-sessionlink").text
		if username == None:
			user_obj['username'] = user_obj['channel-name'].replace(' ', '')
		user_obj['subscribers'] = int(soup_root.find('span', class_="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip").text)
		
		#get all the videos in the channels video tab
		video_elms = soup_videos.find_all('h3', class_="yt-lockup-title")
		videos = []
		r = re.compile('\\\"likeCount\\\":[1-9]+')
		
		#iterate over the videos
		for v in video_elms:
			v_url = "https://youtube.com" + v.find('a')['href']
			
			#creates the bs4 object for the videos page
			videopage = requests.get(v_url).text
			soup_videopage = BeautifulSoup(videopage, 'html.parser')
			
			print(r.search(videopage, 0, len(videopage)))
			
			#get's the likes
			likes = int(r.search(videopage))
			dislikes = int(soup_videopage.find_all('ytd-toggle-button-renderer')[1].find('yt-formatted-string', id="text", class_="style-scope ytd-toggle-button-renderer style-text").text)
			
			#appends an object to the videos array with the data
			videos.append({
				"title": v.find(id="video-title").text,
				"views": int(v.find(id='metadata-line').find_all('span')[0].text[0:1]),
				"url": v_url,
				"likes": likes,
				"dislikes": dislikes,
				"total-votes": likes + dislikes,
				"engagement-ratio": (likes + dislikes) / int(v.find(id='metadata-line').find_all('span')[0].text[0:1])
			})
		
		user_obj['videos'] = videos
		
		#calculates the total amount of views votes and the engagement ratio for the user
		total_views = 0
		total_votes = 0
		engagement_ratio_total = 0
		for v in user_obj['videos']:
			total_views += v['views']
			total_votes += v['total-votes']
			engagement_ratio_total += v['engagement-ratio']
		
		#engagement score
		user_obj['engagement-ratio'] = engagement_ratio_total / len(user_obj['videos'])
		
		return user_obj
	
	#returns all channels from a google search
	def search_channels(self, youtuber):
		if self.exists(youtubers):
			return self.youtubeuserurl + youtuber #if there's a youtube account directly matching your query, then return it
		page = requests.get(self.youtubesearchurl + youtuber) #getting the html of the search page
		self.soup = BeautifulSoup(page, 'html.parser') #beautifulsoup object for parsing page
		channels = []
		#go through all the channel results and add the ones that have a valid url
		for channel in soup.find_all('a', class_='channel-link yt-simple-endpoint style-scope ytd-channel-renderer'):
			if requests.get(self.youtuberooturl + channel['href']) != self.youtube_404:
				channels.append(channel['href'])
		return channels

pyt = Pytube()
print(pyt.user(id="UC_laWT7O377Ktxa2JnDuQnw"))