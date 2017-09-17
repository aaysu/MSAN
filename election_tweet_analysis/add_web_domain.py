from urllib2 import urlopen, Request
from urlparse import urlparse


def modify_user_data(user_d_list):
    """
    Add url domain field to each tweet in each user data object.
    Url domain field contains list of domains corresponding to list of urls.
    """
    for user in user_d_list:
        for tweet in user['tweets']:
            domains = [get_domain_of_url(url) for url in tweet['urls']]
            tweet['domains'] = domains
    return


def get_domain_of_url(url):
    """
    Determine the domain that a url redirects to.
    """
    try:
        request = Request(url)
        request.add_header('User-Agent', 'Resistance is futile')
        response = urlopen(request)
        response_url = response.url
        domain = urlparse(response_url).hostname
        return domain.lower()
    except:
        return "URL_ERROR"
