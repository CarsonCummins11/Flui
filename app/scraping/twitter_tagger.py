from gensim.test.utils import common_texts
from gensim.models import Word2Vec, Phrases
import json
from app.scraping.twitter import TweepyBot
from nltk.tokenize import word_tokenize

#searches using most common words in english as keywords
def build_with_generic_keys():
    build(['the','be','to','of','and','a','in','that','have','I','it','for','not','on','with'])
#call this to get training data and train the model
def build(keywords):
    bot = TweepyBot()
    bot.search(keywords)
    tweets = json.load(open('app/scraping/mldata/twdata.json'))
    data = []
    for tweet in tweets:
        f = tweet.replace("\n", " ")
        temp = [] 
            # tokenize the tweet into words 
        for j in word_tokenize(tweet): 
            temp.append(j.lower()) 
        data.append(temp)
    #train the model
    model = Word2Vec(data,size=100, window=5, min_count=3, workers=4)
    model.save("word2vec.model")

#call this to tag an array of tweets
def tag(tweets):
    model = Word2Vec.load("word2vec.model")
    data = []
    for tweet in tweets:
        f = tweet.replace("\n", " ")
        temp = [] 
            # tokenize the tweet into words 
        for j in tweet.split(): 
            temp.append(j.lower()) 
        data.append(temp)
    model.build_vocab(data, update=True)
    model.train(data, total_examples=model.corpus_count, epochs=model.iter)
    probs = {}
    for tweet in tweets:
        words = word_tokenize(tweet)
        for word in words:
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