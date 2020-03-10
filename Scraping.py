#Citation: https://www.promptcloud.com/blog/how-to-scrape-youtube-data-using-python/
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import sys
import ast
import json
import os
import math
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Input link for now
url = input('Enter Youtube Video Url- ')

#Mozilla browser
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#There should be a for loop that goes through each one of the videos after the user provide a link to 
#their profile, and each one of the video goes through the process down below that generates a rating


#Extracting data from one specific youtube video, right now you have to provide a link, but once the 
#step above is complete, just take those html as the inputs.
soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
video_details = {}
other_details = {}

#Title doens't really matter, but if Carson might use it 
for span in soup.findAll('span',attrs={'class': 'watch-title'}):
    video_details['TITLE'] = span.text.strip() 

#Since Channel is provided, probably useless.
for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
        channelDesctiption = json.loads(script.text.strip())
        video_details['CHANNEL_NAME'] = channelDesctiption['itemListElement'][0]['item']['name']

for div in soup.findAll('div',attrs={'class': 'watch-view-count'}):
    video_details['NUMBER_OF_VIEWS'] = div.text.strip()

for button in soup.findAll('button',attrs={'title': 'I like this'}):
    video_details['LIKES'] = button.text.strip()

for button in soup.findAll('button',attrs={'title': 'I dislike this'}):
    video_details['DISLIKES'] = button.text.strip()

for span in soup.findAll('span',attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}):
    video_details['NUMBER_OF_SUBSCRIPTIONS'] = span.text.strip()

#The hashtags/trending
hashtags = []
for span in soup.findAll('span',attrs={'class': 'standalone-collection-badge-renderer-text'}):
    for a in span.findAll('a',attrs={'class': 'yt-uix-sessionlink'}):
        hashtags.append(a.text.strip())
video_details['HASH_TAGS'] = hashtags



for x in video_details:  
    print(x)
    if x == 'LIKES':
        likes = (int(video_details[x].replace(',','')))
        print(likes)
    elif x == 'NUMBER_OF_VIEWS':
        views = video_details[x]
        views = views.replace(' ','')
        views = views.replace('views','')
        views = views.replace(',','')
        views = (int(views))
        print(views)
    elif x == 'DISLIKES':
        dislikes = (int(video_details[x].replace(',','')))
        print(dislikes)
    elif x == 'NUMBER_OF_SUBSCRIPTIONS':
        Subs = video_details[x]
        Subs = Subs.replace('M','000000')
        Subs = Subs.replace('K','000')
        Subs = Subs.replace('B','000000000')
        Subs = int(Subs)
        print(Subs)
    else:
        print(video_details[x])
    print('')

#however you want to rate it, I havn't thought of one yet
video_details['RATING'] = math.log2((likes - dislikes + views) / Subs**0.8)
print(video_details['RATING'])

#Write to a different file first, although all we need is just a rating for an channel.
with open('data.json', 'w', encoding='utf8') as outfile:
    json.dump(video_details, outfile, ensure_ascii=False,indent=4)

