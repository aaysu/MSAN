import grequests
from urlparse import urlparse

def exception_handler(request, exception):
    return "URL_REQUEST_ERROR"


def get_domain_of_response(response):
    try:
        response_url = response.url
        domain = urlparse(response_url).hostname
        return domain.lower()
    except:
        return "GET_DOMAIN_ERROR"


def modify_user_data(user_d_list):
    # create list of all URLs
    urls = []
    for user in user_d_list:
        for tweet in user['tweets']:
            for url in tweet['urls']:
                urls.append(url)

    # create list of requests
    requests = (grequests.get(url) for url in urls)
    # send requests asynchronously
    responses = grequests.map(requests, exception_handler=exception_handler, size=100)
    # get domains from response
    domains = [get_domain_of_response(response) for response in responses]

    # create dictionary of urls:domains
    url_to_domain = dict(zip(urls, domains))

    # use dictionary to map urls to domains
    for user in user_d_list:
        for tweet in user['tweets']:
            tweet_domains = [url_to_domain[url] for url in tweet['urls']]
            tweet['domains'] = tweet_domains

    return