#pytube object for scraping youtube
from bs4 import BeautifulSoup
import requests
import re

#returns true if the page of the url is one of youtube's 2 404 page
def is404(url):
	return requests.get(url).status_code!=404 #sets the page

def string_to_int(string):
	print(string)
	string = string.replace(',','')
	multipliers = {'K':1000, 'M':1000000, 'B':1000000000}
	if string[-1].isdigit(): # check if no suffix
		return int(string)
	mult = multipliers[string[-1]] # look up suffix to get multiplier
     # convert number to float, multiply by multiplier, then make int
	return int(float(string[:-1]) * mult)
def idFromUsername(username):
	print('uhhh')
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
		if(username is not None):
			id = idFromUsername(username)
			username = None
		'''
		user_obj = { #object of the yt user to be returned
			"username": username,
			"channel-name": None,
			"subscribers": None,
			"videos": None,
			"total-views": None,
			"total-votes": None,
			"engagement-ratio": None
		}
		'''
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
		#soup_root = BeautifulSoup(root, 'html.parser')
		'''
		#setting the channel name, subscribers and username
		user_obj['channel-name'] = soup_root.find('a', class_="spf-link branded-page-header-title-link yt-uix-sessionlink").text
		if username == None:
			user_obj['username'] = user_obj['channel-name'].replace(' ', '')
		user_obj['subscribers'] = string_to_int(soup_root.find('span', class_="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip").text)
		'''
		#get all the videos in the channels video tab
		video_elms = re.compile('watch\?v=(.*?)"').findall(videos)
		print(video_elms)
		videos = []
		
		#iterate over the videos
		for v in video_elms:
			videos.append("https://www.youtube.com/watch?v=" + v)
			'''
			#creates the bs4 object for the videos page
			videopage = requests.get(v_url).text
			soup_videopage = BeautifulSoup(videopage, 'html.parser')
		
			#get's the likes
			f_pos = videopage.find('"likeCount')
			s_pos = f_pos
			while videopage[s_pos] != ',':
				s_pos += 1
			if not videopage[f_pos:s_pos] == '':
				likes = string_to_int(videopage[f_pos:s_pos].replace('"', '').replace('\\', '').replace("likeCount:", ''))
			else: likes = None

			f_pos = videopage.find('"dislikeCount')
			s_pos = f_pos
			while videopage[s_pos] != ',':
				s_pos += 1
			if not videopage[f_pos:s_pos] == '':
				dislikes = int(videopage[f_pos:s_pos].replace('"', '').replace('\\', '').replace("dislikeCount:", ''))
			else: dislikes = None

			#Getting Title
			f_pos = videopage.find('"videoTitle')
			s_pos = f_pos
			while videopage[s_pos] != ',':
				s_pos += 1
			title = videopage[f_pos + 14:s_pos].replace("}",'').replace('"','').replace('\\','')
			
			#get's views
			f_pos = videopage.find('<div class="watch-view-count">') + 30
			s_pos = f_pos
			while videopage[s_pos] != ' ':
				s_pos += 1
			if not videopage[f_pos:s_pos] == '' and not videopage[f_pos:s_pos] == '"':
				views = string_to_int(videopage[f_pos:s_pos])
			else: views = None

			#get's subscribers
			sub_str = 'yt-subscriber-count" title="1" aria-label="1" tabindex="0">'
			f_pos = videopage.find(sub_str) + len(sub_str)
			s_pos = f_pos
			subscribers=None
			while videopage[s_pos] != '<':
				s_pos += 1
			if not videopage[f_pos:s_pos].replace('">', '') == '':
				subscribers = string_to_int(videopage[f_pos:s_pos].replace('">', ''))
			else: 
				subsribers = None

			#appends an object to the videos array with the data
			videos.append({
				"title": title,
				"views": views,
				"url": v_url,
				"likes": likes,
				"dislikes": dislikes,
				"total-votes": None if likes == None or dislikes == None else likes + dislikes,
				"engagement-ratio": None if likes == None or dislikes == None or subscribers==None else (likes + dislikes) / subscribers
			})
		
		user_obj['videos'] = videos
		
		#calculates the total amount of views votes and the engagement ratio for the user
		total_views = 0
		total_votes = 0
		engagement_ratio_total = 0
		for v in user_obj['videos']:
			if not v['views'] == None:
				total_views += v['views']
			if not v['total-votes'] == None:
				total_votes += v['total-votes']
			if not v['engagement-ratio'] == None:
				engagement_ratio_total += v['engagement-ratio']
		
		#engagement score
		user_obj['engagement-ratio'] = engagement_ratio_total / len(user_obj['videos'])
		'''
		return videos
	
	#returns all channels from a google search
	def search_channels(self, youtuber):
		if is404(youtuber):
			return self.youtubeuser + youtuber #if there's a youtube account directly matching your query, then return it
		page = requests.get(self.youtubesearchurl + youtuber) #getting the html of the search page
		self.soup = BeautifulSoup(page, 'html.parser') #beautifulsoup object for parsing page
		channels = []
		#go through all the channel results and add the ones that have a valid url
		for channel in self.soup.find_all('a', class_='channel-link yt-simple-endpoint style-scope ytd-channel-renderer'):
			if not is404(self.youtuberoot + channel['href']):
				channels.append(channel['href'])
		return channels