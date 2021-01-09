from app.scraping.youtube import YoutubeBot
from app.scraping.tagger import Tagger
from nltk.tokenize import sent_tokenize,word_tokenize
class YT_Tagger:
    def __init__(self):
        self.bot = YoutubeBot()
        self.tagger = Tagger()
    def tag(self,id):
        print(self.bot.all_videos(id))
        return self.tag_videos(self.bot.all_videos(id))
    def tag_videos(self,videos):
        allwords = ''
        for video in videos:
            caps = self.bot.get_captions(video)
            caps = caps.replace('\\n',' ')+'.'
            allwords+=caps
        sents = sent_tokenize(allwords)
        data = []
        for sent in sents:
            data+=word_tokenize(sent)
        return self.tagger.tag(data)