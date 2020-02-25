from youtube import YoutubeBot
from tagger import Tagger
from nltk.tokenize import sent_tokenize,word_tokenize
class YT_Tagger:
    def __init__(self):
        self.bot = YoutubeBot()
        self.tagger = Tagger()
    def tag(self,video):
        caps = self.bot.get_captions(video)
        caps = caps.replace('\\n',' ')
        sents = sent_tokenize(caps)
        data = []
        for sent in sents:
            data+=word_tokenize(sent)
        return self.tagger.tag(data)
tg = YT_Tagger()
print(tg.tag('https://www.youtube.com/watch?v=6z7GQewK-Ks'))