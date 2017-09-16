from textblob import TextBlob
import re
import string
from nltk.stem import PorterStemmer
import nltk
from sklearn.feature_extraction import stop_words

def clean_tweet(tweet):
    # takes a list of tweet strings
    # returns a stemmed, tokenized list of words,
    # lowercase, strip punctuation, remove stop words and < 3 in length
    # all the re.sub's are a bit redundant but the OR condition was being stubborn
    # takes a filtered list of tweets and returns a list of stems
    temp = re.sub('http[^\s]*', ' ', tweet)
    temp = re.sub('@[^\s]*', ' ', temp)
    temp = re.sub('#[^\s]*', ' ', temp)
    pattern = re.compile('[' + string.punctuation + '0-9\\r\\t\\n]')
    temp = re.sub(pattern, ' ', temp)
    temp = temp.lower()
    temp = temp.encode('ascii', 'ignore')
    tokens = nltk.word_tokenize(temp)
    token_list = [word for word in tokens if len(word) > 2]
    filtered_list = [word for word in token_list if word not in stop_words.ENGLISH_STOP_WORDS]
    stemmer = PorterStemmer()
    stemmed_list = [stemmer.stem(word) for word in filtered_list]
    return stemmed_list


def modify_user_data(user_d_list):
    """
    Add topic domain field to each tweet in each user data object.
    Topic domain field contains list of topics from initial list found in the clean tweet text.
    """
    politics_text = ['hillary', 'clinton', 'donald', 'trump', 'taxes', 'immigration',
                     'abortion', 'trade', 'election', 'vote', 'campaign']
    stemmer = PorterStemmer()
    politics_list = [stemmer.stem(word) for word in politics_text]
    for user in user_d_list:
        for tweet in user['tweets']:
            raw_text = tweet['text']
            stemmed_list = clean_tweet(raw_text)
            intersect = [val for val in stemmed_list if val in politics_list]
            if len(intersect) > 0:
                tweet['topic'] = list(set(intersect))
            else:
                tweet['topic'] = []
    return