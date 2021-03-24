
import os
import json
import sys
import yaml
import random
import tweepy
import geocoder
import what3words
from word_parser import word_parser
from word_check import word_check

# Load Configuration File
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['twitter_auth']['api_key'], cfg['twitter_auth']['api_secret_key'])
auth.set_access_token(cfg['twitter_auth']['access_token'], cfg['twitter_auth']['secret_access_token'])

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_trending(loc):
    
    t_words = [] # Empty List to Hold Words

    # Trends for Specific Country
    g = geocoder.osm(loc) # Object with Location's Latitude and Longitude
    closest_loc = api.trends_closest(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])

    # Extract Trending Tags
    for value in trends:
        for trend in value['trends']:
            value = word_parser(trend['name'])
            if type(value) == list:
                t_words.extend(value)
            else:
                t_words.append(value)
    
    # Word List Cleanup
    t_words = [i for i in t_words if len(i) > 1] # remove single characters entries
    t_words = [x.lower() for x in t_words] # lowercase all list
    t_words = word_check(t_words) # remove any words in list not in english dictionary
    three_words = random.sample(t_words, 3) # randomly select three words
    three_word_str = '.'.join(three_words) # join list items

    return three_word_str


def get_lat_long(words):
    # Create What3Words API object
    geocoder = what3words.Geocoder(str(cfg['what3words']['api_key']))

    # Three words to coordinates test
    result = geocoder.convert_to_coordinates(words)

    return str(result['coordinates']['lat']), str(result['coordinates']['lng'])


def get_map_url(latitude, longitude):
    # get image map of coordinates - should be a function
    center = latitude + ',' + longitude
    zoom = 15
    size = "800x400"
    maptype = "roadmap" # roadmap, satellite, hybrid, terrain
    url = "https://maps.googleapis.com/maps/api/staticmap?" + "center=" + center + "&zoom=" + \
        str(zoom) + "&size=" + size + "&maptype=" + maptype + "&key=" + cfg['google_static_map']['api_key']
    
    return url


if __name__ == "__main__":
    word_str = get_trending("United States")
    print(word_str)
    latitude, longitude = get_lat_long(word_str)
    print(latitude, ',', longitude)
    
    