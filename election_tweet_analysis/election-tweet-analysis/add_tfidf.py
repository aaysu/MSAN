import sys
import re
import os
import tweepy
import numpy as np
import string
import nltk
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from twitter_api_wrapper import *



def writing_tweets_to_file(tweets):
    # os.chdir(sys.argv[0])
    tweets = " ".join(tweets)
    filename = 'twitter_user'
    f = open(filename, 'w')
    f.write(tweets)
    f.close()
    return filename



def clean_tweets(text):
    # takes a list of tweet strings
    # returns a stemmed, tokenized list of words,
    # lowercase, strip punctuation, remove stop words and < 3 in length
    text = [re.sub('http[^\s]*', ' ', t) for t in text]
    text = [re.sub('@[^\s]*', ' ', t) for t in text]
    text = [re.sub('#[^\s]*', ' ', t) for t in text]
    pattern = re.compile('[' + string.punctuation + '0-9\\r\\t\\n]')
    text = [re.sub(pattern, ' ', t) for t in text]
    text = [t.lower() for t in text]
    t_list = [t.encode('ascii', 'ignore') for t in text]
    t_list = ", ".join(t_list)
    tokens = nltk.word_tokenize(t_list)
    token_list = [word for word in tokens if len(word) > 2]
    filtered_list = [word for word in token_list if word not in stop_words.ENGLISH_STOP_WORDS]
    stemmer = PorterStemmer()
    stemmed_list = [stemmer.stem(word) for word in filtered_list]
    return stemmed_list


def tfidf_for_tweets(corpus, filename):
    # takes twitter user id, file previously made with their tweets (in a roundabout way),
    # and the corpus file and returns a list of tuples of tfidf on words in tweets
    tfidf = TfidfVectorizer(input='filename',
                            analyzer='word',
                            preprocessor=None,
                            decode_error='ignore',
                            tokenizer=None,
                            stop_words=None)
    tweet_matrix = tfidf.fit_transform([corpus, filename])                             # tfidf matrix corpus + tweet file
    small_matrix = tweet_matrix[1]                                                     # tfidf matrix of the tweet file
    word_index = np.nonzero(small_matrix)[1]                                           # index of words
    words = [tfidf.get_feature_names()[i].encode('ascii') for i in word_index]
    values = [small_matrix[0, w] for w in word_index]
    tupely_tupes = zip(words, values)
    sort_tupes = sorted(tupely_tupes, key=lambda x: x[1], reverse= True)
    limit_tupes = [tupe for tupe in sort_tupes if tupe[1] >= 0.09]
    return limit_tupes


# ###for example####
# n = 10
# twitter_id = 15846407                               # Ellen DeGeneres :)
# corpus = sys.argv[5]                                # corpus of lots o tweets



def big_tfidf_on_tweets(list_of_tweets, corpus):
    # takes list of tweets, returns list of tuples of words and tfidf scores
    tweets = clean_tweets(list_of_tweets)
    filename = writing_tweets_to_file(tweets)
    scores = tfidf_for_tweets(corpus, filename)
    return scores

def modify_user_data(user_data):
    for user in user_data:
        list_of_tweets = [tweet['text'] for tweet in user['tweets']]
        tuples = big_tfidf_on_tweets(list_of_tweets, 'corpus')
        user['tfidf'] = tuples




# api = authorize_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)
# raw_tweets = redundant_tweet_grab_function(twitter_id, n)                              # get tweets
# tweets = clean_tweets(raw_tweets)                                                      # clean tweets
# writing_tweets_to_file(tweets)                                                         # write cleaned tweets to file
# print tfidf_for_tweets(corpus)                                                         # tfidf and words need to store in dict
# print type(raw_tweets)