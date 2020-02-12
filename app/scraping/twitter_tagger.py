from gensim.test.utils import common_texts
from gensim.models import Word2Vec, Phrases

def build():
    bigram_transformer = Phrases(common_texts)
    model = Word2Vec(bigram_transformer[common_texts], min_count=1)
    model.save("word2vec.model")
def tag(username):
    