from bs4 import BeauitfulSoup
import requests

def is404(url):
	page = requests.get(url)
	soup = BeautifulSoup(page, 'html.parser')
	error_404 = soup.find(id="error-page-hh-illustration")
	error_404_channel = soup.find(class_="channel-empty-message banner-message")
	if error_404 != None or error_404_channel != None:
		return True;
	return False;

class Pytube:
	def __init__(self):
		self.youtuberoot = "https://youtube.com/"
		self.youtubeuser = self.youtubeuser + "user/"
		self.youtubeid = self.youtubechannel + "channel/"
	
	def user(self, username=None, id=None):
		root = None
		root_url = None
		
		user_obj = {
			"username": None,
			"channel-name": None
			"subscribers": None,
			"videos": None,
			"total-views": None,
			"total-votes": None,
			"engagement-ratio": None
		}
		
		u_exists = is404(self.youtubeuser + username)
		id_exists = is404(self.youtubechannel + id)
		
		if u_exists:
			root = requests.get(self.youtubeuser + username)
			root_url = self.youtubeuser + username + "/"
		elif id_exists:
			root = requests.get(self.youtubechannel + id)
			root_url = self.youtubechannel + id + "/"
		
		if root == None:
			return "Unable to find user or id"
		
		videos = requests.get(root + "videos/")
		
		soup_root = BeautifulSoup(root, 'html.parser')
		soup_videos = BeautifulSoup(videos, 'html.parser')
		
		user_obj['channel-name'] = soup_root.find(class_="style-scope ytd-channel-name")
		if username == None:
			user_obj['username'] = user_obj['channel-name'].replace(' ', '')
		user_obj['subsribers'] = int(soup_root.find(id="subscriber-count").text[0:2])
		
		video_elms = soup_videos.find_all('ytd-grid-video-renderer')
		videos = []
		
		for v in video_elms:
			v_url = "https://youtube.com" + v.find(id="thumbnail").href
			
			videopage = requests.get(v_url)
			soup_videopage = BeautifulSoup(videopage, 'html.parser')
			
			likes = int(soup_videopage.find_all('ytd-toggle-button-renderer')[0].find('yt-formatted-string', id="text", class_="style-scope ytd-toggle-button-renderer style-text").text)
			dislikes = int(soup_videopage.find_all('ytd-toggle-button-renderer')[1].find('yt-formatted-string', id="text", class_="style-scope ytd-toggle-button-renderer style-text").text)
			
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
		
		total_views = 0
		total_votes = 0
		engagement_ratio_total = 0
		for v in user_obj['videos']:
			total_views += v['views']
			total_votes += v['total-votes']
			engagement_ratio_total += v['engagement-ratio']
		
		user_obj['total-views'] = total_views / len(user_obj['videos'])
		user_obj['total-votes'] = total_votes / len(user_obj['videos'])
		user_obj['engagement-ratio'] = engagement_ratio_total / len(user_obj['videos'])
		
		return user_obj
		
		