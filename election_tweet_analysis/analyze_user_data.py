from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
from os import path
from nltk.stem import PorterStemmer
import matplotlib.pylab as plt
import numpy as np


def get_top_domains(user_d_list):

    # get all domains
    domains = []
    for user in user_d_list:
        for tweet in user['tweets']:
            domains = domains + tweet['domains']

    # count
    domain_counts = Counter(domains)

    # sort
    sorted_counts = sorted(((v, k) for k, v in domain_counts.items()), reverse=True)

    # print
    for count in sorted_counts[0:12]:
        print count[1], count[0]

    return


def get_top_hashtags(user_d_list):

    # get all domains
    hashtags = []
    for user in user_d_list:
        for tweet in user['tweets']:
            hashtags = hashtags + tweet['hashtags']

    # count
    hashtag_counts = Counter(hashtags)

    # sort
    sorted_counts = sorted(((v, k) for k, v in hashtag_counts.items()), reverse=True)

    # print
    for count in sorted_counts[0:10]:
        print count[1], count[0]

    return

def make_cloud(user_data, hashtag_str):
    # get all tfidfs
    word_list= []
    d = path.dirname(__file__)
    for user in user_data:
       tuple_list  = user['tfidf']
       word_list = word_list + list(zip(*tuple_list)[0])
    word_string = " ".join(word_list)
    if hashtag_str == "NeverTrump":
        mask = imread(path.join(d, "hillary1.png"))

    else:
        mask = imread(path.join(d, "trump1.png"))
    wordcloud = WordCloud( background_color = 'white',
                                mask = mask,
                                stopwords=STOPWORDS,
                                width = 1200,
                                height =1000
                                ).generate(word_string)

    image_colors = ImageColorGenerator(mask)
    fig = plt.figure()
    plt.imshow(wordcloud.recolor(color_func=image_colors))

    # plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    fig.savefig('wordcloud'+ hashtag_str + '.png', dpi = fig.dpi)


def avg_sentiment(user_d_list, hashtag_str):
    sentiment_list = []
    for user in user_d_list:
        for tweet in user['tweets']:
            sentiment = tweet['sentiment']
            sentiment_list.append(sentiment)
    print sum(sentiment_list)/len(sentiment_list)
    for sentiment in sentiment_list:
        if sentiment == 0:
            del sentiment
    plt.hist(sentiment_list)
    plt.title('Histogram of Sentiments: #%s' % hashtag_str)
    plt.show()
    return


def filter_by_topic(user_d_list, topic_list = []):
    # returns all "non-political" tweets by default
    politics_text = ['hillary', 'clinton', 'donald', 'trump', 'taxes', 'immigration',
                     'abortion', 'trade', 'election', 'vote', 'campaign']
    stemmer = PorterStemmer()
    if topic_list == ['all']:
        topic_list = politics_text
    else:
        topic_list = [val for val in topic_list if val in politics_text]
    topic_list_print = ', '.join(topic_list)
    # variables to track total users/tweets and users/tweets who pass the filter
    userct = 0
    tweetct = 0
    userpass = 0
    tweetpass = 0
    sentiment = 0
    for user in user_d_list:
        tweetadd = 0
        userct += 1
        for tweet in user['tweets']:
            tweetct += 1
            if topic_list == []:
                if len(tweet['topic']) == 0:
                    tweetadd += 1
                    sentiment += tweet['sentiment']
            else:
                topic_list = [stemmer.stem(word) for word in topic_list]
                intersect = [val for val in topic_list if val in tweet['topic']]
                if len(intersect) > 0:
                    tweetadd += 1
                    sentiment += tweet['sentiment']
        if tweetadd != 0:
            tweetpass += tweetadd
            userpass += 1
    avgSentiment = float(sentiment) / tweetpass
    avgUser = float(userpass) / userct
    avgTweet = float(tweetpass) / tweetct
    print 'Looking at political topics from the following list: \n%s\nAverage sentiment: %f\nUser ratio:' \
           '%f\nTweet ratio: %f' % (topic_list_print, avgSentiment, avgUser, avgTweet)
    return