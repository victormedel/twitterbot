#!/usr/bin/env python
# twitterbot/bot/w3w_tweet.py
import os
import json
import sys
import time
import yaml
import emoji
import random
import tweepy
import geocoder
import logging
import requests
import pycountry
import threading
import what3words
from datetime import datetime
from word_parser import word_parser
from word_check import word_check
from config import create_twitter_api, create_google_api, create_w3w_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

WAIT_SECONDS = 60 # 7200


def get_trending(t_api, loc):
    
    trending_words = [] # Empty List to Hold Words

    # Trends for Specific Country
    g = geocoder.osm(loc) # Object with Location's Latitude and Longitude
    closest_loc = t_api.trends_closest(g.lat, g.lng)
    trends = t_api.trends_place(closest_loc[0]['woeid'])

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


def get_loc(w_api, words):
    # Create What3Words API object
    geocoder = what3words.Geocoder(w_api)

    # Get nearest location based on what3words word suggestion
    result = geocoder.autosuggest(words)

    # Get values from item in set ranked #1
    country_abv = result['suggestions'][0]['country']
    nearest_loc = result['suggestions'][0]['nearestPlace']
    sugg_words = result['suggestions'][0]['words']

    # Get latitude and longitude for suggested words
    coord = geocoder.convert_to_coordinates(sugg_words)
    latitude = str(coord['coordinates']['lat'])
    longitude = str(coord['coordinates']['lng'])

    country = pycountry.countries.get(alpha_2=country_abv)

    return sugg_words, nearest_loc , country.name, latitude, longitude


def map_generator(g_api, center):
    # get image map of coordinates - should be a function
    zoom = 18
    size = "800x400"
    maptype = "hybrid" # roadmap, satellite, hybrid, terrain
    url = "https://maps.googleapis.com/maps/api/staticmap?" + "center=" + center + "&zoom=" + \
        str(zoom) + "&size=" + size + "&maptype=" + maptype + "&key=" + g_api
    
    # get image from url
    req = requests.get(url) 

    # save image to file
    f = open('map_img.png', 'wb') 
    f.write(req.content) 
    f.close() 


def twitter_post(t_api, sugg_words, nearest_loc , country, latitude, longitude):
        
    # Upload Image
    media = t_api.media_upload('map_img.png')

    # Post tweet with image
    tweet = 'Interesting! @what3words is using the random words ///' + sugg_words + \
            ' to identify a three meter square area on earth near: ' + '\n' + \
            emoji.emojize(':round_pushpin:') + nearest_loc + ' (' + country + ')' + '\n\n' + \
            '#what3words #Random #Location #AnythingInteresting?'
    
    place_id = nearest_loc + ',' + country
    t_api.update_status(status=tweet, media_ids=[media.media_id], lat=latitude, long=longitude, place_id=place_id)



def main():

    t_api = create_twitter_api()
    g_api = create_google_api()
    w_api = create_w3w_api()

    # ticker = threading.Event()
    # while not ticker.wait(WAIT_SECONDS):

    # Post to Twitter
    trd_words = get_trending(t_api, "United States")
    sugg_words, nearest_loc, country, latitude, longitude = get_loc(w_api, trd_words)
    center = latitude + ',' + longitude
    map_generator(g_api, center)
    # twitter_post(t_api, sugg_words, nearest_loc , country, latitude, longitude)

    print(sugg_words)
    print(nearest_loc, '(', country, ')')
    print(center)

    # Establish current date and time
    now = datetime.now()
    dt_str = now.strftime("%m/%d/%Y %H:%M:%S")
    logger.info('Tweet posted on: ' + str(dt_str))


if __name__ == "__main__":
    main()
