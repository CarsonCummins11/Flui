from wikipedia2vec import Wikipedia2Vec
model = Wikipedia2Vec.load('wiki_tagger.pkl')
newtag = input('input tag')
try:
    model.get_word_vector(newtag.lower())
except:
    try:
        model.get_entity_vector(newtag)
    except:
        try:
            model.get_entity_vector(newtag.lower())
        except:
            print('adding failed')
            quit()
if newtag not in open('app/scraping/mldata/tags.txt','r').readlines():
    with open('app/scraping/mldata/tags.txt','a') as f:
        f.write('\n'+newtag)
else:
    print('tag already exists')