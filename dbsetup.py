#Sets up the mongo database
from pymongo import MongoClient

client = MongoClient()
db = client['matcher']
#Loops over 'companies.txt' and creates profiles for each
with open('dummydata/companies.txt') as f:
    for row in f:
        prof = {'company':row[0],
        'user':row[1],
        'pass':generate_password_hash('p'),
        'desc':'No Description',
        'email':'No Email',
        'image':'',
        'tags':''}
        db['advertisers'].insert_one(prof)
#Loops over 'influencers.txt' and creates profiles for each
with open('dummydata/influencers.txt') as f:
    for row in f:
        prof = {'company':row[0],
        'user':row[1],
        'pass':generate_password_hash('p'),
        'desc':'No Description',
        'email':'No Email',
        'image':'',
        'tags':''}
        db['influencers'].insert_one(prof)