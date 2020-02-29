import threading
from app.scraping import twitter_tagger
from app import db
from app.scraping import youtube_tagger
from app.scraping import instagram_tagger
class WorkflowController:
    twwork=[]
    instawork=[]
    ytwork=[]
    twthread = False
    ytthread=False
    instathread=False
    def dotwwork(self):
        twtag = twitter_tagger.TW_tagger()
        while True:
            if len(self.twwork)>0:
                user = self.twwork.pop(0)
                tags_new= twtag.tag(user)
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
    def doytwork(self):
        yttag = youtube_tagger.YT_tagger()
        while True:
            if len(self.ytwork)>0:
                user = self.ytwork.pop(0)
                tags_new= yttag.tag(user)
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
    def doinstawork(self):
        yttag = instagram_tagger.Insta_tagger()
        while True:
            if len(self.instawork)>0:
                user = self.instawork.pop(0)
                tags_new= yttag.tag(user)
                tags_cur = db['influencers'].find_one({'user':user})['tags']
                tags = ''
                for tag in tags_new:
                    if tag not in tags_cur:
                        tags+=tag+','
                tags=tag+tags_cur
                db['influencers'].update({'user':user},{'$set':{'tags':tags}})
    def tagTWUser(self,user):
        twwork.append(user)
        if(self.twthread==False):
            threading.start_new_thread(self.dotwwork)
            self.twthread=True
    def tagYTUser(self,user):
        ytwork.append(user)
        if(self.ytthread==False):
            threading.start_new_thread(self.doytwork)
            self.ytthread=True
    def tagInstaUser(self,user):
        instawork.append(user)
        if(self.instathread==False):
            threading.start_new_thread(self.doinstawork)
            self.instathread=True
        

