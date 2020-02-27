from app.scraping.instagram import InstagramBot
from app.scraping.tagger import Tagger
from nltk.tokenize import sent_tokenize,word_tokenize
class Insta_Tagger:
    def __init__(self):
        self.bot = InstagramBot()
        self.tagger = Tagger()
    def tag(self,username):
        posts = self.bot.get_data(username)
        text = ''
        for key in posts.keys():
            if not 'postInfo' in key:
                text+=posts[key]+'.'
        data = []
        sents = sent_tokenize(text)
        for sent in sents:
            data+=word_tokenize(sent)
        return self.tagger.tag(data)