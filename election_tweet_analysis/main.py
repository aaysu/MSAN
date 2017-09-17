import sys
from twitter_api_wrapper import *
from pretty_print import pretty
import add_web_domain_parallelized
import add_sentiment
import analyze_user_data
import add_tfidf
import add_topic

# authorize api and get api tweepy object
consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
access_token = sys.argv[3]
access_token_secret =sys.argv[4]

def authorize_twitter_api(consumer_key, consumer_secret,
                          access_token, access_token_secret):
    """Author twitter API object."""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

api = authorize_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

def analyze_users_with_hashtag(hashtag_str, N_USERS=10, N_TWEETS=10):
    # user ids
    print "Getting user IDs for #" + hashtag_str
    user_ids = get_n_user_ids_from_tweets_by_hashtag(api, hashtag = hashtag_str, n = N_USERS)
    # get user data

    print "Getting user data for #" + hashtag_str
    user_data = [get_raw_user_data_from_userid(api, user_id, ntweets = N_TWEETS) for user_id in user_ids]

    # add meta data
    print "Adding tfidf data for #" + hashtag_str
    add_tfidf.modify_user_data(user_data)
    print "Adding domain data for #" + hashtag_str
    add_web_domain_parallelized.modify_user_data(user_data)
    print "Adding sentiment data for #" + hashtag_str
    add_sentiment.modify_user_data(user_data)
    print "Adding tweet topic data for #" + hashtag_str
    add_topic.modify_user_data(user_data)

    # analyze data
    print "Analyzing top web domains for #" + hashtag_str
    analyze_user_data.get_top_domains(user_data)
    print "Analyzing top hashtags for #" + hashtag_str
    analyze_user_data.get_top_hashtags(user_data)
    print "Making word cloud for #" + hashtag_str
    analyze_user_data.make_cloud(user_data, hashtag_str)
    print "Get average sentiment and histogram for #" + hashtag_str
    analyze_user_data.avg_sentiment(user_data, hashtag_str)
    print "Analyzing political topic sentiment and frequency for #" +hashtag_str
    analyze_user_data.filter_by_topic(user_data, ['all'])

# > 180 users total will require 15 minute wait...
# > 300 total tweets (N_USERS * N_TWEETS) will require 15 minute wait
# > 300 tweets per user will cause assert error
analyze_users_with_hashtag("NeverTrump", N_USERS=10, N_TWEETS=10)
analyze_users_with_hashtag("MakeAmericaGreatAgain", N_USERS=10, N_TWEETS=10)


