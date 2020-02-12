from gensim.test.utils import common_texts
from gensim.models import Word2Vec, Phrases
import json
from twitter import TweepyBot

#searches using most common words in english as keywords
def build_with_generic_keys():
    build(['the','be','to','of','and','a','in','that','have','I','it','for','not','on','with'])
#call this to get training data and train the model
def build(keywords):
    bot = TweepyBot()
    bot.search(keywords)
    tweets = json.load(open('mldata/twdata.json'))
    data = []
    for tweet in tweets:
        f = tweet.replace("\n", " ")
        temp = [] 
            # tokenize the sentence into words 
        for j in tweet.split(): 
            temp.append(j.lower()) 
        data.append(temp)
    model = Word2Vec(data,size=100, window=5, min_count=1, workers=4)
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
build_with_generic_keys()