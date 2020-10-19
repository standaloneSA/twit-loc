#!/usr/bin/env python

import sys
import twitter
import read_config
import json
from urllib.parse import quote as urlquote
import geograpy
import geocoder

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
    # user location is freetext, so we will scrape it for location
    if tweet.user.location is not None:
        #TODO: check for coords

        tweet_coords = dict()
        # Use geograpy
        try:
            p = geograpy.Extractor(text = tweet.user.location)
        except Exception as err:
            print("... problem looking up location %s: %s" % (tweet.user.location, str(err)))
            return
        p.find_entities()
        loc = geograpy.Locator()
        city = loc.locateCity(p.places)
        if city:
            try:
                location_name = "%s, %s, %s" % (str(city.name), str(city.region.name), str(city.country.name))
                g = geocoder.arcgis(location_name)
                tweet_coords = {"lat": g.current_result.lat, "lon": g.current_result.lng} 
                # print("DEBUG: location_name: %s" % location_name)
                # print("DEBUG: %s" % str(tweet_coords))
            except Exception as err:
                print("... problem geocoding %s: %s" % (str(city), str(err)))
                location_name = "Unknown"
        else:
            location_name = "Unknown"
        if tweet_coords.get('lat') is None or tweet_coords.get('lon') is None:
            tweet_coords['lat'] = "0"
            tweet_coords['lon'] = "0"
            location_name = "Unknown"
        print("Location: %s (%s,%s)" % (location_name, tweet_coords['lat'], tweet_coords['lon']))
    print("User Timezone: %s" % str(tweet.user.time_zone))
    pass

if __name__ == '__main__':
    twit = twit_init()
    try:
        #tweet = twit.GetHomeTimeline(count=1)[0]
        tweets = search(twit, sys.argv[1], count=10)
    except twitter.error.TwitterError as err:
        print("Error: %s" % str(err))
        pass
    #print(tweet.AsJsonString())
    for tweet in tweets:
        print(" ")
        print("-=-=-")
        print("%s - https://twitter.com/%s/status/%s" % (tweet.user.screen_name, tweet.user.screen_name, tweet.id))
        print(tweet.text)
        find_tweet_geo(tweet)

