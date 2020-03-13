#scraping bot for instagram
#uncomment this when running with python3 -m flask run(running the whole app)
from app.scraping.authentication.auth import auth_data #this is for local testing with the command python3 instagram.py(testing just this script)
from instagram_private_api import Client, ClientCompatPatch, ClientError, ClientLoginError
from app import app,db
import json
from lxml import html
import requests
from app.scraping.regex import extract_urls
from random import randint
from datetime import timedelta, date

def user_data(username):
    return requests.get('https://www.instagram.com/' + username +'/?__a=1').json()

#found this on stackoverflow
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class InstagramBot:
    #Log into instagram and init api object with auth data
    def __init__(self):
        self.api = Client(autopatch = True, authenticate = True, username = auth_data['insta_auth']['username'], password = auth_data['insta_auth']['password'])
        self.user_id = auth_data['insta_auth']["id"]
        self.potential_influencers = []
        self.indata = {}
        self.engagement_score = 0
        self.code_length = 6
        self.code_valid_time = 5

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

    #for returning text without added captions to improve ML models
    def make_ml_friendly(self,text):
        text = text.replace('Image may contain: ','')
        text = text.replace('one or more people','')
        return text

    #creates a json object with the message to be sent and returns a code
    def get_code_message(self):
        code = random_with_N_digits(self.code_length)
        code_message = '''
            Here is your temporary code: ''' + code + '''

            If you did not link your account to Flui, ignore this message.
        '''
        return {
            "message": code_message,
            "code": code
        }

    # sends a message with a confirmation code to their account
    # fluiuser = their flui username
    # username = instagram username
    # influencer specifies if the user is an influencer or not
    # instagram, twitter, youtube specify the platform
    #
    # Ex:
    #   ...code setting their instagram username....
    #   create_user_code(their-flui-username, their-instagram-username, instagram=True)
    #
    def create_user_code(self, fluiuser, username, influencer=True, instagram=False, twitter=False, youtube=False):
        if instagram:
            message = self.get_code_message()
            self.send_message(message['message'], username)
            db['influencers' if influencer else 'advertisers'].update({'user':fluiuser},{'$set':{'insta-confirm-code':message['code']}})
            db['influencers' if influencer else 'advertisers'].update({'user':fluiuser},{'$set':{'confirm-code-validuntil': date.today() + timedelta(days=self.code_valid_time)}})

    #Sends a message to a user
    def send_message(self, message, target):
        urls = extract_urls(message) #gets urls from text with hellish regex
        item_type = "link" if urls else "text" #sets the type of message depending on if the 'message' contains urls
        user = user_data(target) #get's the user object
        try:
            self.api.send_direct_item(item_type, user['graphq1']['id'], text=message, thread=None, urls=urls) #sendsthe message
        except:
            print("Failed to send message")
    
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