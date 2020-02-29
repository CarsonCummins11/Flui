#scraping bot for instagram
#uncomment this when running with python3 -m flask run(running the whole app)
#from app.scraping.authentication.auth import auth_data
from app.scraping.authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError
import json
from lxml import html
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
            ratios.append(post['like_count'] / info['user']['follower_count'])
            self.engagement_score = sum(ratios) / len(ratios)
            v = 1+1
        self.engagement_score = round(self.engagement_score, 4)
        return self.engagement_score

    def make_ml_friendly(self,text):
        text = text.replace('Image may contain: ','')
        text = text.replace('one or more people','')
        return text

    def get_data(self, username):
        posts = self.api.username_feed(username)
        i = 0
        results = {}
        for post in posts['items']:
            if(post['caption']):
                results['postInfo'+str(i)] = post['caption']["media_id"]
                post_url = 'https://www.instagram.com/p/' + post['code']
                info = requests.get(post_url).text
                if not 'accessibility_caption":"' in info:
                    print('no alt')
                else:
                    alt = (info.split('accessibility_caption":"'))[1].split('"')[0]
                    results['capt'+str(i)] = post['caption']['text']
                    results['img'+str(i)] = self.make_ml_friendly(alt)
                i+=1
        return results
