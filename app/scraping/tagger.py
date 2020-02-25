import gensim.downloader as api
from os import path
from gensim.models.word2vec import Word2Vec
class Tagger:
    def __init__(self):
        if path.exists('tagger.model'):
            print('model already made')
            self.model = Word2Vec.load('tagger.model')
        else:
            data = api.load("text8")
            print('building model')
            self.model = Word2Vec(data,size=100, window=5, min_count=3, workers=4)
            self.model.save('tagger.model')
    def tag(self,words):
        #generate average similarities to each tag
        sims = {}
        for word in words:
            if word in self.model.wv.vocab:
                tags = open("app/scraping/mldata/tags.txt")
                for tag in tags:
                    tag = tag.replace('\n','').lower()
                    if tag in sims:
                        sims[tag] = [sims[tag][0]+self.model.similarity(word,tag),sims[tag][1]+1]
                    else:
                        sims[tag] = [self.model.similarity(word,tag),1]
        for tag in sims.keys():
            sims[tag] = sims[tag][0]/sims[tag][1]
        sims={k: v for k, v in sorted(sims.items(), key=lambda item: item[1])}
        tags = []
        for k in sims.keys():
            tags.append(k)
        return tags[-4:]
    