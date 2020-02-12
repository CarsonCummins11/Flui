from gensim.test.utils import common_texts
from gensim.models import Word2Vec, Phrases
from nltk.tokenize import sent_tokenize, word_tokenize
import json

#call this to train the model
def build():
    tweets = json.load('mldata/twdata.json')
    all_data = []
    for tweet in tweets:
        f = s.replace("\n", " ")
        data = []
        # iterate through each sentence in the file 
        for i in sent_tokenize(f): 
            temp = [] 
            # tokenize the sentence into words 
            for j in word_tokenize(i): 
                temp.append(j.lower()) 
            data.append(temp)
        all_data.append(data)
    model = Word2Vec(all_data,size=100, window=5, min_count=1, workers=4)
    model.save("word2vec.model")

#call this to tag an array of tweets
def tag(tweets):
    model = Word2Vec.load("word2vec.model")
    probs = {}
    for tweet in tweets:
        words = tweet.split()
        for word in words:
            avgsim = 0
            tags = open('mldata/tags.txt')
            for tag in tags:
                probs[tag]+=model.similarity(word,tag)
            tags.close()
    tags = open('mldata/tags.txt')
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