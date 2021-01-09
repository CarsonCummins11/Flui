import threading
from app.scraping.instagram import InstagramBot
from app.scraping import twitter_tagger
from app import db
from app.scraping import youtube_tagger
from app.scraping import instagram_tagger
from queue import Queue


def combine_vote_tables(t_new,t_cur):
    ret = {}
    for k in t_new:
        if k in t_cur.keys():
            ret[k] = t_new[k]+t_cur[k]
        else:
            ret[k] = t_new[k]
    for k in t_cur:
        if k in t_new.keys():
            ret[k] = t_new[k]+t_cur[k]
        else:
            ret[k] = t_cur[k]
    return ret
twwork = Queue()
instawork= Queue()
ytwork = Queue()
ytthread=False
twthread=False
instathread=False
def dotwwork():
    global twwork
    twtag = twitter_tagger.TW_Tagger()
    while True:
        user = twwork.get()
        tagging = twtag.tag(user)
        tags_new= tagging['plain']
        tags_cur = db['influencers'].find_one({'twitter':user})['tags']
        tags = ''
        for tag in tags_new:
            if tag not in tags_cur:
                tags+=tag+','
        tags=tags+tags_cur
        db['influencers'].update({'twitter':user},{'$set':{'tags':tags}})
        tags_votes = tagging['verbose']
        tags_votes_cur = db['influencers'].find_one({'twitter':user})['votes']
        tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
        db['influencers'].update({'twitter':user},{'$set':{'votes':tags_votes}})
def doytwork():
    global ytwork
    yttag = youtube_tagger.YT_Tagger()
    while True:
        user = ytwork.get()
        tagging = yttag.tag(user)
        tags_new= tagging['plain']
        tags_cur = db['influencers'].find_one({'youtube':user})['tags']
        tags = ''
        for tag in tags_new:
            if tag not in tags_cur:
                tags+=tag+','
        tags=tags+tags_cur
        db['influencers'].update({'youtube':user},{'$set':{'tags':tags}})
        tags_votes = tagging['verbose']
        tags_votes_cur =  db['influencers'].find_one({'youtube':user})['votes']
        tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
        db['influencers'].update({'youtube':user},{'$set':{'votes':tags_votes}})
def doinstawork():
    global instawork
    yttag = instagram_tagger.Insta_Tagger()
    while True:
        user = instawork.get()
        tagging = yttag.tag(user)
        tags_new= tagging['plain']
        tags_cur = db['influencers'].find_one({'instagram':user})['tags']
        tags = ''
        for tag in tags_new:
            if tag not in tags_cur:
                tags+=tag+','
        tags=tags+tags_cur
        db['influencers'].update({'instagram':user},{'$set':{'tags':tags}})
        tags_votes = tagging['verbose']
        tags_votes_cur =  db['influencers'].find_one({'instagram':user})['votes']
        tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
        db['influencers'].update({'instagram':user},{'$set':{'votes':tags_votes}})
def tagTWUser(user):
    global twwork
    global twthread
    twwork.put(user)
    if(twthread==False):
        threading.Thread(target=dotwwork).start()
        self.twthread=True
def tagYTUser(user):
    global ytwork
    global ytthread
    ytwork.put(user)
    if(ytthread==False):
        threading.Thread(target=doytwork).start()
        ytthread=True
def tagInstaUser(user):
    global instawork
    global instathread
    instawork.put(user)
    if(instathread==False):
        threading.Thread(target=doinstawork).start()
        instathread=True