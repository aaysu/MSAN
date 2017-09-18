import nltk
from sklearn.feature_extraction import text
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

# tokenize description and return a non-unique list of tokenized words
# normalize to lowercase, drop words of length < 3, remove stop words
def tokenize(ticket):
    words = nltk.word_tokenize(ticket.lower())
    final = []
    for i in range(len(words)):
        if len(words[i]) > 2:
            if words[i] not in text.ENGLISH_STOP_WORDS:
                final.append(words[i])
    return final

# given a list of tokens/words, return a new list with each word stemmed using a porterstemmer
def stemwords(words):
    stemmed = []
    for word in words:
        try:
            stemmed.append(PorterStemmer().stem(word))
        except:
            stemmed.append(word)
    return stemmed

# setup for tfidf vectorizer
def prepare(ticket):
    return stemwords(tokenize(ticket))

tfidf = TfidfVectorizer(input='content',  # argument to transform() is a list of descriptions
                        decode_error='strict',
                        analyzer='word',
                        tokenizer=prepare,  # clean, tokenize, stem
                        stop_words='english')  # strip out stop words

def cluster(filtered, description, keep):
    filtered = filtered['description'].tolist()
    filtered.append(description)
    matrix = tfidf.fit_transform(filtered)
    num = max(2, len(filtered)/5)
    km = KMeans(n_clusters=num)
    km.fit(matrix)
    clusters = km.labels_.tolist()
    group = clusters[-1]
    del clusters[-1]
    del filtered [-1]
    df_cluster = pd.DataFrame.from_items([('index', keep), ('cluster', clusters), ('description', filtered)])
    df_match = df_cluster.loc[df_cluster['cluster'] == group]
    return df_match['index']
