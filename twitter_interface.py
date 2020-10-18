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

def find_tweet_geo(tweet):
    """
    Returns coordinates for a tweet. Since not all tweets have coordinates set, we have to 
    take some creative liberties. Here is how this works: 
   
    1) If there are geo coordinates set, use those. 
    2) If the user has a location set, try to look up the coordinates for that. 
    3) Default fallback is 0,0
    
    This is actually available if you pay for it:
    https://developer.twitter.com/en/docs/twitter-api/v1/enrichments/overview/profile-geo
    """
    # Things we care about: 
    print("Tweet Coordinates: %s" % str(tweet.coordinates))
    print("Tweet language: %s" % str(tweet.lang))
    print("User Location: %s" % str(tweet.user.location))
    print("User Timezone: %s" % str(tweet.user.time_zone))
    pass

if __name__ == '__main__':
    twit = twit_init()
    tweet = twit.GetHomeTimeline(count=1)[0]
    print(tweet.AsJsonString())
    print("-=-=-")
    print("%s - https://twitter.com/%s/status/%s" % (tweet.user.screen_name, tweet.user.screen_name, tweet.id))
    print(tweet.text)
    find_tweet_geo(tweet)

