import threading
from app.scraping import twitter_tagger
from app import db
from app.scraping import youtube_tagger
from app.scraping import instagram_tagger

def combine_vote_tables(t_new,t_cur):
    ret = {}
    for k in t_new:
        if k in t_cur.keys():
            ret[k] = t_new[k]+t_cur[k]
        else:
            ret[k] = t_new[k]
    return ret

class WorkflowController:
    def __init__(self):
        self.twwork=[]
        self.instawork=[]
        self.ytwork=[]
        self.twthread = False
        self.ytthread=False
        self.instathread=False
    def dotwwork(self):
        twtag = twitter_tagger.TW_tagger()
        while True:
            if len(self.twwork)>0:
                user = self.twwork.pop(0)
                tagging = twtag.tag(user)
                tags_new= tagging['plain']
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
                tags_votes = tagging['verbose']
                tags_votes_cur = db['influencers'].find_one({'user':user})['votes']
                tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
                db['influencers'].update({'user':user},{'$set':{'votes':tags_votes}})
    def doytwork(self):
        yttag = youtube_tagger.YT_tagger()
        while True:
            if len(self.ytwork)>0:
                user = self.ytwork.pop(0)
                tagging = yttag.tag(user)
                tags_new= tagging['plain']
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
                tags_votes = tagging['verbose']
                tags_votes_cur =  db['influencers'].find_one({'user':user})['votes']
                tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
                db['influencers'].update({'user':user},{'$set':{'votes':tags_votes}})
    def doinstawork(self):
        yttag = instagram_tagger.Insta_tagger()
        while True:
            if len(self.instawork)>0:
                user = self.instawork.pop(0)
                tagging = yttag.tag(user)
                tags_new= tagging['plain']
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
                tags_votes = tagging['verbose']
                tags_votes_cur =  db['influencers'].find_one({'user':user})['votes']
                tags_votes = combine_vote_tables(tags_votes,tags_votes_cur)
                db['influencers'].update({'user':user},{'$set':{'votes':tags_votes}})
    def tagTWUser(self,user):
        self.twwork.append(user)
        if(self.twthread==False):
            #threading.Thread(self.dotwwork).start()
            self.twthread=True
    def tagYTUser(self,user):
        self.ytwork.append(user)
        if(self.ytthread==False):
            #threading.Thread(target=self.doytwork).start()
            self.ytthread=True
    def tagInstaUser(self,user):
        self.instawork.append(user)
        if(self.instathread==False):
            #threading.Thread(self.doinstawork).start()
            self.instathread=True
        

