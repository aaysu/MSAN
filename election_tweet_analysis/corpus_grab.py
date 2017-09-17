import sys
import tweepy
import sys
import re
import string
import nltk
from sklearn.feature_extraction import stop_words
from nltk.stem import PorterStemmer
from twitter_api_wrapper import *
from collections import defaultdict



def authorize_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    # authorize twitter API object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def tweet_ids_and_tweets(twitter_id, maxpull, total):
    # get list of tweets and tweet id's
    tweet_set = set()
    tweets = handle_rate_limit(api.user_timeline, "user_timeline", screen_name = twitter_id, count = maxpull)# first grab from twitter
    for tweet in tweets:                                         # making a set of tuples of tweet.id and tweet.text
        tweet_set.add((tweet.id, tweet.text))
    min_id = min(zip(*tweet_set)[0])                             # finding the last tweet
    while len(tweet_set) < total:
        more_tweets = handle_rate_limit(api.user_timeline, "user_timeline", screen_name = twitter_id, count=maxpull, max_id=min_id)
        for tweet in more_tweets:
            tweet_set.add((tweet.id, tweet.text))
        min_id = min(zip(*tweet_set)[0])                         # getting the oldest pulled tweet id

    tweet_list = list(tweet_set)
    tweet_id_list, tweet_list = zip(*tweet_list)
    return tweet_list

TRY_COUNT=defaultdict(int)
def handle_rate_limit(api_call, api_call_name, **args):
    """
    Handle Twitter rate limit exception by waiting 15 minutes
    then trying API call again.
    """
    global TRY_COUNT
    result = None
    while result is None:
        try:
            TRY_COUNT[api_call_name] += 1
            result = api_call(**args)
        except tweepy.RateLimitError:
            print "API limit hit for " + api_call_name + ". Gonna chill for 15 minutes."
            print TRY_COUNT
            time.sleep(15 * 60)
    return result


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


consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
access_token = sys.argv[3]
access_token_secret =sys.argv[4]


total = 3000
twitter_id = "CocaCola"
twitter_id2 = "Gap"
maxpull = 300
filename = 'corpus'


api = authorize_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)


tweet_list = tweet_ids_and_tweets(twitter_id, maxpull, total)
tweet_list2 = tweet_ids_and_tweets(twitter_id2, maxpull, total)

large_corpus = clean_tweets(tweet_list)
large_corpus2 = clean_tweets(tweet_list2)
large_corpus += large_corpus2

large_corpus = " ".join(large_corpus)

f = open(filename, 'w')
f.write(large_corpus)
f.close()

