from pymongo import MongoClient

client = MongoClient()
db = client['matcher']
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