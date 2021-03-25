
import os
import json
import sys
import yaml
import random
import tweepy
import geocoder
import requests
import what3words
from word_parser import word_parser
from word_check import word_check

# Load Configuration File
if os.path.exists('test_config.yml'):
    config_file = 'test_config.yml'

else:
    config_file = 'config.yml'

with open(config_file, "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['twitter_auth']['api_key'], cfg['twitter_auth']['api_secret_key'])
auth.set_access_token(cfg['twitter_auth']['access_token'], cfg['twitter_auth']['secret_access_token'])

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_trending(loc):
    
    trending_words = [] # Empty List to Hold Words

    # Trends for Specific Country
    g = geocoder.osm(loc) # Object with Location's Latitude and Longitude
    closest_loc = api.trends_closest(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])

    # Extract Trending Tags
    for value in trends:
        for trend in value['trends']:
            value = word_parser(trend['name'])
            if type(value) == list:
                trending_words.extend(value)
            else:
                trending_words.append(value)
    
    # Word List Cleanup
    trending_words = [i for i in trending_words if len(i) > 2] # remove single characters entries
    trending_words = [x.lower() for x in trending_words] # lowercase all list
    
    trending_words = word_check(trending_words) # remove any words in list not in english dictionary

    three_words = random.sample(trending_words, 3) # randomly select three words
    three_word_str = '.'.join(three_words) # join list items

    return three_word_str


def get_lat_long(words):
    # Create What3Words API object
    geocoder = what3words.Geocoder(str(cfg['what3words']['api_key']))

    # Three words to coordinates test
    result = geocoder.autosuggest(words)

    country = result['suggestions'][0]['country']
    nearest = result['suggestions'][0]['nearestPlace']
    suggested_words = result['suggestions'][0]['words']

    return country, nearest, suggested_words


def get_map_url(center):
    # get image map of coordinates - should be a function
    zoom = 15
    size = "800x400"
    maptype = "hybrid" # roadmap, satellite, hybrid, terrain
    url = "https://maps.googleapis.com/maps/api/staticmap?" + "center=" + center + "&zoom=" + \
        str(zoom) + "&size=" + size + "&maptype=" + maptype + "&key=" + cfg['google_static_map']['api_key']
    
    r = requests.get(url) 

    # wb mode is stand for write binary mode 
    f = open('map_results.png', 'wb') 
    
    # r.content gives content, 
    # in this case gives image 
    f.write(r.content) 
    
    # close method of file object 
    # save and close the file 
    f.close() 

    return url


if __name__ == "__main__":
    word_str = get_trending("United States")
    country, location, suggested_words = get_lat_long(word_str)
    get_map_url(str(location + ',' + country))

    print(country)
    print(location)
    print(' ')
    print('Twitter Trending Words: ', word_str)
    print('What3Words Suggestion:', suggested_words)
    


    
    