from textblob import TextBlob

def modify_user_data(user_d_list):
    """
    Add url domain field to each tweet in each user data object.
    Url domain field contains list of domains corresponding to list of urls.
    """
    for user in user_d_list:
        for tweet in user['tweets']:
            blob = TextBlob(tweet['text'])
            tweet['sentiment'] = blob.sentiment.polarity
    return