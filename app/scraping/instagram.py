#scraping bot for instagram
#uncomment this when running with python3 -m flask run(running the whole app)
#from app.scraping.authentication.auth import auth_data
from authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError
import json
from lxml import html
import requests
from io import BytesIO
from PIL import Image
import pickle
import base64
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
        i = 0
        results = {}
        for post in posts['items']:
            results['postInfo'+str(i)] = post['caption']["media_id"]
            post_url = 'https://www.instagram.com/p/' + post['code']
            page = requests.get(post_url)
            tree = html.fromstring(page.content)
            img_url = tree.xpath('/html/head/meta[11]/@content')[0]
            response = requests.get(img_url)
            img = Image.open(BytesIO(response.content))
            stri = base64.b64encode(response.content).decode('utf-8')
            # results['desc'] = description
            results['capt'+str(i)] = post['caption']['text']
            results['img'+str(i)] = stri
            # print(results)
            i+=1
        json.dump(results, open("mldata/instadata.json", 'w+'))