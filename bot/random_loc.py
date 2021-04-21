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

WAIT_SECONDS = 1800
RESTART_WAIT = 120
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
    sugg_words = result['suggestions'][0]['words']

    # Get latitude and longitude for suggested words
    logger.info('Getting location information based on lat-long')
    coord = geocoder.convert_to_coordinates(sugg_words)
    latitude = str(coord['coordinates']['lat'])
    longitude = str(coord['coordinates']['lng'])
    country_abv = coord['country']
    nearest_loc = coord['nearestPlace']
    sugg_words_final = coord['words']

    logger.info('Converting country abbreviation to full country name')
    country = pycountry.countries.get(alpha_2=country_abv)

    logger.info('Returning location data')


    if any(elem is None for elem in [sugg_words_final, nearest_loc, country.name, latitude, longitude]) or nearest_loc == '':
        logger.info('None type or empty variable detected, restarting process in two minutes')
        time.sleep(RESTART_WAIT) # sleep for 2 minutes before attempting again
        main()

    else:
        print('>>>>', sugg_words_final, ',', nearest_loc, ',', country.name, ',', latitude, ',', longitude, '<<<<')
        return sugg_words_final, nearest_loc, country.name, latitude, longitude


def map_generator(g_api, latitude, longitude):
    # datetime object containing current date and time to be used in filename
    now = datetime.now()

    # format date and time string to mmddYY_HMS
    date_time_str = now.strftime("%m%d%Y_%H%M%S")

    # get image map of coordinates
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
    file_name = 'map_img_' + date_time_str +'.png'
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
        os.remove(file_name)
        time.sleep(RESTART_WAIT) # sleep for 2 minutes before attempting again
        main()

    else:
        return file_name


def twitter_post(t_api, file_name, trd_words, sugg_words, nearest_loc , country, latitude, longitude):
    logger.info('Using all gathered and generated data to compose and publish post')
    
    # Post Text
    logger.info('Generating text for post')
    status = emoji.emojize(':compass:') + ' @what3words address ///' + sugg_words + ' can be found near: \n' + \
             emoji.emojize(':round_pushpin:') + nearest_loc + ' (' + country + ')' + '\n\n' + \
             emoji.emojize(':world_map:') + ' What\'s your 3 word address? \n\n' + \
             '#what3words'

    try:
        logger.info('Prepare Image for Upload')
        media = t_api.media_upload(file_name)

        logger.info('Post to Twitter')
        t_api.update_status(status=status, media_ids=[media.media_id], lat=latitude, long=longitude)

    except tweepy.TweepError as e:
        print(e.api_code)
        print(getExceptionMessage(e.reason))
        time.sleep(RESTART_WAIT)
        main()

    logger.info('Removing image')
    os.remove(file_name)


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
    logger.info('...wainting before for posting again')
    time.sleep(WAIT_SECONDS)


if __name__ == "__main__":
    while True:
        main()
