from app.scraping.twitter import TweepyBot
from app.scraping.tagger import Tagger
from nltk.tokenize import sent_tokenize,word_tokenize
class TW_Tagger:
    def __init__(self):
        self.bot = TweepyBot()
        self.tagger = Tagger()
    def tag(self,username):
        tweets = '. '.join(self.bot.get_tweets(username))
        tweets = tweets.replace('\\n',' ')
        sents = sent_tokenize(tweets)
        data = []
        for sent in sents:
            data+=word_tokenize(sent)
        return self.tagger.tag(data)
tg = TW_Tagger()
print(tg.tag('jack'))
        

