#scraping bot for instagram
#uncomment this when running with python3 -m flask run(running the whole app)
#from app.scraping.authentication.auth import auth_data
from app.scraping.authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError
import json
import requests
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
            #ratios.append(post['like_count'] / info['follower_count'])
        #self.engagement_score = sum(ratios) / len(ratios)
            v = 1+1
    def store_data(self, username):
        posts = self.api.username_feed(username)
        for post in posts['items']:
            results = {}
            results['postInfo'] = post['caption']["media_id"]
            post_url = 'https://www.instagram.com/p/' + post['code']
            html = requests.get(post_url)
            print(html.text)
            # results['desc'] = description
            results['capt'] = post['caption']['text']
            # print(results)
        json.dump(results, open("instadata.json", 'w+'))
    '''def get_media_id(url):
        r = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
        media_id = r.json()['media_id']
        return media_id'''
#testing commands, remove when finished
insta_bot = InstagramBot()
#insta_bot.set_engagement_ratio(auth_data['insta_auth']['username'])
insta_bot.store_data('ty.greenwood')