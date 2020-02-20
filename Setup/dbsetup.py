#Sets up the mongo database
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import random

client = MongoClient()
db = client['matcher']

def randomtags():
    tags = [ line for line in open('dummydata/tags.txt')]
    return random.choice(tags)+','+random.choice(tags)+','+random.choice(tags)+','+random.choice(tags)
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
i=0
#Loops over 'companies.txt' and creates profiles for each
with open('dummydata/companies.txt') as f:
    for row in f:
        prof = {'company':row[:-1],
        'user':row[:-1],
        'pass':generate_password_hash('p'),
        'desc':'No Description',
        'email':'No Email',
        'image':'',
        'tags':randomtags()}
        db['advertisers'].insert_one(prof)
        printProgressBar(i,2100)
        i+=1
#Loops over 'influencers.txt' and creates profiles for each
with open('dummydata/influencers.txt') as f:
    for row in f:
        prof = {'name':row[:-1],
        'user':row[:-1],
        'pass':generate_password_hash('p'), #generates password hash from entered password
        'desc':'No Description',
        'email':'No Email',
        'image':'', #file path?
        'instagram':'No Instagram',
        'youtube':'No YouTube',
        'twitter':'No Twitter',
        'tags':randomtags()}
        db['influencers'].insert_one(prof)
        printProgressBar(i,2100)
        i+=1
