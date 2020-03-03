from os import path
from wikipedia2vec import Wikipedia2Vec
import numpy as np
#donwload model file from http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_300d.pkl.bz2
def cossim(vec1,vec2):
        a = np.array(vec1)
        b = np.array(vec2)
        # manually compute cosine similarity
        dot = np.dot(a, b)
        norma = np.linalg.norm(a)
        normb = np.linalg.norm(b)
        return dot / (norma * normb)
class Tagger:
    def __init__(self):
        if path.exists('wiki_tagger.pkl'):
            print('model already made')
            self.model=Wikipedia2Vec.load('wiki_tagger.pkl')
        else:
            print('no model found')
    def tag(self,words):
        tags = [k.replace('\n','') for k in open('app/scraping/mldata/tags.txt','r').readlines()]
        text = ' '+' '.join(words)+' '
        counts = {}
        for item in self.model.dictionary:
            try:
                if ' '+item.text.lower()+' ' in text.lower():
                    counts[item.text]=text.lower().count(' '+item.text.lower()+' ')
            except:
                if ' '+item.title.lower()+' ' in text.lower():
                    if item.title in counts:
                        counts[item.text]=text.lower().count(' '+item.title.lower()+' ')
        print(counts)
        sims = {}
        for tag in tags:
            tagvec = []
            try:
                tagvec = self.model.get_word_vector(tag.lower()).tolist()
            except:
                try:
                    tagvec = self.model.get_entity_vector(tag).tolist()
                except: 
                    try:
                        tagvec = self.model.get_entity_vector(tag.lower()).tolist()
                    except:
                        print(tag)

            for item in counts:
                vector=[]
                try:
                    vector = self.model.get_word_vector(item).tolist()
                except:
                    vector = self.model.get_entity_vector(item).tolist()
                try:
                    sims[tag] += counts[item]*cossim(vector,tagvec)
                except:
                    sims[tag] = counts[item]*cossim(vector,tagvec)
        count = 0
        for k in counts:
            count+=counts[k]
        for k in sims:
            sims[k]/=count
        sims = {k: v for k, v in sorted(sims.items(), key=lambda item: item[1])}
        ret_top4 = list(sims.keys())[-4:]
        ret = []
        for k in ret_top4:
            print(sims[k])
            if(sims[k]>.7):
                ret.append(k)
        return ret