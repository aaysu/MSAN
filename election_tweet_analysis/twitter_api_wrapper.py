import time
import tweepy
from collections import defaultdict


def get_tweets_by_hashtag(api, hashtag, count=1, beforeID=None):
    """
    Get [count] number of tweets with given hashtag. Limit is 100.
    Return (tweet_id, author_id, author_screenname) list of tuples.
    """
    if count > 100: count=100  # limit count to 100

    if beforeID is None:
        tweets_by_hashtag = api.search("%23" + hashtag, count=str(count))
    else:
        tweets_by_hashtag = api.search("%23" + hashtag, count=str(count), max_id=str(beforeID-1))

    tweet_ids = [tweet.id for tweet in tweets_by_hashtag]
    user_ids = [tweet.author.id for tweet in tweets_by_hashtag]

    return list(zip(tweet_ids, user_ids))


def get_n_user_ids_from_tweets_by_hashtag(api, hashtag, n):
    """
    Get n total number of tweets with given hashtag.
    Need to keep calling get_tweets_by_hashtag until n is reached.
    Return list of non-duplicated user IDs.
    Note we are limited to 100 tweets per request and 450 requests every 15 minutes (45,000 total tweets).
    """

    user_ids = set()  # use set to automatically remove duplicates
    min_tweet_id = None

    # keep making call until desired number of users is reached
    while len(user_ids) < n:
        more_tweets = get_tweets_by_hashtag(api, hashtag, count=n, beforeID=min_tweet_id)
        min_tweet_id = min(zip(*more_tweets)[0])

        for tweet_id, user_id in more_tweets:
            user_ids.add(user_id)

    # turn set into list of userIDs
    user_id_list = []
    for id in user_ids:
        user_id_list.append(id)

    return user_id_list




def get_raw_user_data_from_userid(api, user_id, ntweets):
    """
    Given user ID, returns data dictionary for that user with:
            * uid
            * language
            * location
            * screen_name
            * list of dictionaries of last ntweets number of tweets:
                * text of tweet
                * list of URLs contained tweet
                * list of hashtags contained in tweet
                * source of tweet (e.g. android, ipad, etc)

        Limited to 180 get user requests.
        Limited to 500 get_timeline requests.
    """

    assert ntweets <= 300, "Can not request more than 300 tweets per user."

    user_dict = {}  # initialize dictionary of user data

    # data that comes from api.get_user request
    user = handle_rate_limit(api.get_user, "get_user", user_id=user_id)

    user_dict["uid"] = user.id
    user_dict["screen_name"] = user.name
    user_dict["language"] = user.lang
    user_dict["location"] = user.location

    # data that comes from api.user_timeline request
    user_timeline = handle_rate_limit(api.user_timeline, "user_timeline", user_id=user_id, count=ntweets)

    user_dict["tweets"] = get_all_tweet_data_from_timeline(user_timeline)


    return user_dict

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


def get_all_tweet_data_from_timeline(timeline):
    """Create list with dictionary for each tweet in timeline."""
    tweet_data = []
    for status in timeline:
        tweet_data.append(get_tweet_data_from_status(status))
    return tweet_data

def get_tweet_data_from_status(status):
    """Create dictionary for the given tweet (aka status)"""
    tweet_dict = {}
    tweet_dict["text"] = status.text
    tweet_dict["source"] = status.source
    tweet_dict["hashtags"] = [hashtag_data["text"] for hashtag_data in status.entities["hashtags"]]
    tweet_dict["urls"] = [url_data["expanded_url"] for url_data in status.entities["urls"]]
    return tweet_dict






