#scraping bot for instagram
#uncomment this when running with python3 -m flask run(running the whole app)
from app.scraping.authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from app import app,db
import json
from lxml import html
import requests
from app.scraping.regex import extract_urls
import re

def user_data(username):
    return requests.get('https://www.instagram.com/' + username +'/?__a=1').json()

class InstagramBot:
    #Log into instagram and init api object with auth data
    def __init__(self):
        self.user_id = auth_data['insta_auth']["id"]
        self.potential_influencers = []
        self.indata = {}
        self.engagement_score = 0

    #calculate the engagement ratio for a specific user
    def set_engagement_ratio(self, username):
        hp = requests.get('https://www.instagram.com/'+username+'/').text
        follower_count = int(re.compile('"(.*?) Followers').findall(hp)[0])
        k = re.compile('edge_liked_by":{"count":(.*?)}').findall(hp)
        likes = sum([int(x) for x in k])/len(k)
        self.engagement_score = likes/follower_count
        return self.engagement_score

    #for returning text without added captions to improve ML models
    def make_ml_friendly(self,text):
        text = text.replace('Image may contain: ','')
        text = text.replace('one or more people','')
        return text
    def get_data(self, username):
        posts = self.username_feed(username)
        i = 0
        results = {}
        for post in posts:
            results['capt'+str(i)] = post[0]
            results['img'+str(i)] = post[1]
            i+=1
        return results
    def username_feed(self,username):
        posts = []
        hp = requests.get('https://www.instagram.com/'+username+'/').text
        captions = re.compile('"text":"(.*?)"').findall(hp)
        descs = re.compile('"accessibility_caption":"(.*?)"').findall(hp)
        descs = [self.make_ml_friendly(x) for x in descs]
        return zip(captions,descs)


        

