#!/usr/bin/env python
# twitter-bot/bot/w3w_tweet.py
import os
import sys
import time
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

WAIT_SECONDS = 3600
LOCATION = "United States"


def get_trending(t_api, loc):
    logger.info('Retrieving and parsing trending topics into seperate words')
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
    logger.info('Cleaning up word list')
    trending_words = [i for i in trending_words if len(i) > 2] # remove single characters entries
    trending_words = [x.lower() for x in trending_words] # lowercase all list
    
    logger.info('Removing words that do no appear in the english dictionary')
    trending_words = word_check(trending_words) # remove any words in list not in english dictionary
    
    logger.info('Randomly selecting three words from the composed list')
    three_words = random.sample(trending_words, 3) # randomly select three words
    three_word_str = '.'.join(three_words) # join list items

    logger.info('Returning three word list')
    return three_word_str


def get_loc(w_api, words):
    # Create What3Words API object
    logger.info('Creating What3Words API Object')
    geocoder = what3words.Geocoder(w_api)

    # Get nearest location based on what3words word suggestion
    result = geocoder.autosuggest(words)

    # Get values from item in set ranked #1
    logger.info('Extracting information from What3Words object')
    country_abv = result['suggestions'][0]['country']
    nearest_loc = result['suggestions'][0]['nearestPlace']
    sugg_words = result['suggestions'][0]['words']

    # Get latitude and longitude for suggested words
    logger.info('Getting latitude and longitude for the three words suggested')
    coord = geocoder.convert_to_coordinates(sugg_words)
    latitude = str(coord['coordinates']['lat'])
    longitude = str(coord['coordinates']['lng'])

    logger.info('Converting country abbreviation to full country name')
    country = pycountry.countries.get(alpha_2=country_abv)

    logger.info('Returning location data')

    if nearest_loc == '':
        logger.info('Nearest location blank, restarting process')
        time.sleep(120) # sleep for 2 minutes before attempting again
        main()

    else:
        return sugg_words, nearest_loc , country.name, latitude, longitude


def map_generator(g_api, latitude, longitude):
    # get image map of coordinates - should be a function
    logger.info('Retrieving map image')
    center = latitude + ',' + longitude
    zoom = 16
    size = "800x400"
    maptype = "hybrid" # roadmap, satellite, hybrid, terrain
    url = "https://maps.googleapis.com/maps/api/staticmap?" + "center=" + center + "&zoom=" + \
        str(zoom) + "&size=" + size + "&maptype=" + maptype + "&key=" + g_api
    
    req = requests.get(url)

    # Store image file to be used for post
    logger.info('Storing map image to used for Twitter post')
    file_name = '..\map_img.png'
    f = open(file_name, 'wb') 
    f.write(req.content) 
    f.close()

    logger.info('Retrieving image size')
    file_stats = os.stat(file_name)
    file_size = file_stats.st_size/1024
    logger.info('File size: ' + str(file_size))

    logger.info('Returning file name for map')

    if file_size < 100:
        logger.info('Potential low quality map image, restarting process')
        time.sleep(120) # sleep for 2 minutes before attempting again
        main()

    else:
        return file_name


def twitter_post(t_api, file_name, trd_words, sugg_words, nearest_loc , country, latitude, longitude):
    logger.info('Using all gathered and generated data to compose and publish post')
    
    # Post Text
    logger.info('Generating text for post')
    status =  emoji.emojize(':fire:') + ' 3 random words from trending topics in the US today are:\n' + \
               trd_words + '\n\n' + \
               emoji.emojize(':gear:') + ' Modifying these words to:\n' + \
               sugg_words + '\n\n' + \
              '@what3words has identified a 3m square area on earth near: ' + '\n' + \
               emoji.emojize(':round_pushpin:') + nearest_loc + ' (' + country + ')' + '\n\n' + \
              emoji.emojize(':house:') + ' What is your 3 word address? \n\n' + \
               emoji.emojize(':world_map:') + ' #what3words'

    logger.info('Post to Twitter')
    # Upload Image
    media = t_api.media_upload(file_name)

    # Post Tweet
    t_api.update_status(status=status, media_ids=[media.media_id], lat=latitude, long=longitude)


def main():

    logger.info('Generating API keys')
    t_api = create_twitter_api()
    g_api = create_google_api()
    w_api = create_w3w_api()

    # Post to Twitter
    logger.info('Execution begins here')
    trd_words = get_trending(t_api, LOCATION)
    sugg_words, nearest_loc, country, latitude, longitude = get_loc(w_api, trd_words)
    file_name = map_generator(g_api, latitude, longitude)
    twitter_post(t_api, file_name, trd_words, sugg_words, nearest_loc , country, latitude, longitude)

    # Establish current date and time
    now = datetime.now()
    dt_str = now.strftime("%m/%d/%Y %H:%M:%S")
    logger.info('Tweet posted on: ' + str(dt_str))
    logger.info('Done.')


if __name__ == "__main__":
    while True:

        try:
            main()

        except Exception:
            print('Something broke, please restart application')
        
        time.sleep(WAIT_SECONDS)
