from os import path
from wikipedia2vec import Wikipedia2Vec
import numpy as np
import re
import string
#donwload model file from http://wikipedia2vec.s3.amazonaws.com/models/en/2018-04-20/enwiki_20180420_300d.pkl.bz2
def cossim(vec1,vec2):
        a = np.array(vec1)
        b = np.array(vec2)
        dot = np.dot(a, b)
        norma = np.linalg.norm(a)
        normb = np.linalg.norm(b)
        return (dot / (norma * normb))**3
common_words = ["people","things","part","are","like","a","about","after","all","also","an","and","any","as","at","back","be","because","but","by","can","come","could","do","even","first","for","from","get","give","go","good","have","he","her","him","his","how","I","if","in","into","it","its","just","know","like","look","make","me","most","my","new","no","not","now","of","on","one","only","or","other","our","out","over","say","see","she","so","some","take","than","that","the","their","them","then","there","these","they","think","this","time","to","two","up","us","use","want","way","we","well","what","when","which","who","will","with","would","you","your"]
class Tagger:
    def __init__(self):
        if path.exists('wiki_tagger.pkl'):
            print('model already made')
            self.model=Wikipedia2Vec.load('wiki_tagger.pkl')
        else:
            print('no model found')
    def tag(self,words):
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        words = [regex.sub('',word).lower() for word in words]
        words = words = [word for word in words if word not in common_words]
        tags = [k.replace('\n','') for k in open('app/scraping/mldata/tags.txt','r').readlines()]
        text = ' '+' '.join(words)+' '
        print(text)
        counts = {}
        for item in self.model.dictionary:
            try:
                if ' '+item.text.lower()+' ' in text.lower():
                    counts[item.text]=text.lower().count(' '+item.text.lower()+' ')
            except:
                if ' '+item.title.lower()+' ' in text.lower():
                    if item.title in counts:
                        counts[item.title]=text.lower().count(' '+item.title.lower()+' ')
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
                        print(tag+' isn\'nt recognized')

            for item in counts:
                vector=[]
                try:
                    vector = self.model.get_word_vector(item).tolist()
                except:
                    vector = self.model.get_entity_vector(item).tolist()
                try:
                    sims[tag] += counts[item]*cossim(vector,tagvec)
                except KeyError:
                    sims[tag] = counts[item]*cossim(vector,tagvec)
        sims = {k: v for k, v in sorted(sims.items(), key=lambda item: item[1])}
        klist = list(sims.keys())[-4:]
        total = sum(counts.items())
        ret = {}
        for k in klist:
            ret[k] = (sims[k]/total)*100
        returnable = {'verbose': ret,'plain':klist}
        return ret