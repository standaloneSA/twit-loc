#!/usr/bin/env python

import twitter
import read_config
import json
from urllib.parse import quote as urlquote

def twit_init():
    s = read_config.get_secrets()
    twit = twitter.Api(
        access_token_key=s['access_token'],
        access_token_secret=s['access_token_secret'],
        consumer_key=s['api_key'],
        consumer_secret=s['api_secret_key']
        )
    return twit


def get_tweet(twit, user, count=1):
    data = twit.GetUserTimeline(
        screen_name=user,
        count=count
        )
    return data

def _url_builder(**kwargs):
    """ Build the twitter search """
    url = ""
    for key, value in kwargs.items():
        if url != "":
            url += "&"
        url += "%s=%s" % (urlquote(key), urlquote(value))
    return url

def search(twit, query, count=1, **kwargs):
    """ 
    Searches twitter for the query, and returns a list of <count> tweets.
    <since> specifies how long back to look. It is optional. 
    
    Note: 
    This is just some sugar. You can totally command the twit.GetSearch()
    yourself, using the following docs:
    https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
    """
    url = _url_builder(q=query, result_type="recent", count=str(count), **kwargs)
    return twit.GetSearch(raw_query=url)

if __name__ == '__main__':
    mytwit = twit_init()
    print(search(mytwit, '#spacex'))

