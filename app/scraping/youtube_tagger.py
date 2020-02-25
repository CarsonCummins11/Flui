from gensim.test.utils import common_texts
from gensim.models import Word2Vec, Phrases
from nltk.tokenize import sent_tokenize,word_tokenize
def tokenize(cap):
    ret = []
    k = sent_tokenize(cap)
    for sent in k:
        ret.append(word_tokenize(sent))

#call this to get training data and train the model
def build(cap):
    data = tokenize(cap)
    model = Word2Vec(data,size=100, window=5, min_count=3, workers=4)
    model.save("word2vec.model")

#call this to tag a caption string
def tag(cap):
    model = Word2Vec.load("word2vec.model")
    data = tokenize(cap)
    model.build_vocab(data, update=True)
    model.train(data, total_examples=model.corpus_count, epochs=model.iter)
    probs = {}
    for sent in data:
        for word in sent:
            avgsim = 0
            tags = open('app/scraping/mldata/tags.txt')
            for tag in tags:
                probs[tag]+=model.similarity(word,tag)
            tags.close()
    tags = open('app/scraping/mldata/tags.txt')
    length=0
    for line in tags:
        length+=1
    for key,value in probs:
        probs[key]=value/length
    tags.close()
    final_tags = []
    for key,val in probs:
        if(val>.99):
            final_tags.append(key)
    return final_tags