import tweepy
import yaml
import os
import json
import sys
import geocoder
from word_parser import word_parser

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['twitter_auth']['api_key'], cfg['twitter_auth']['api_secret_key'])
auth.set_access_token(cfg['twitter_auth']['access_token'], cfg['twitter_auth']['secret_access_token'])

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_trending(loc):
    # Empty List to Hold Words
    trending_words = []

    # Available Locations
    available_loc = api.trends_available()
    # writing a JSON file that has the available trends around the world
    with open("available_locs_for_trend.json","w") as wp:
        wp.write(json.dumps(available_loc, indent=1))

    # Trends for Specific Country
    # loc = sys.argv[1]     # location as argument variable 
    g = geocoder.osm(loc) # getting object that has location's latitude and longitude

    closest_loc = api.trends_closest(g.lat, g.lng)
    trends = api.trends_place(closest_loc[0]['woeid'])

    # 
    for value in trends:
        for trend in value['trends']:
            value = word_parser(trend['name'])
            if type(value) == list:
                trending_words.extend(value)
            else:
                trending_words.append(value)
            # print(trend['name'])
    
    # List cleanup
    trending_words = [i for i in trending_words if len(i) > 1]
    trending_words = [x.lower() for x in trending_words]
    print(trending_words)




# API Authentication Check
# try:
#     api.verify_credentials()
#     print("Authentication OK")

# except Exception:
#     print("Error during authentication")

# Upload Image
# media = api.media_upload("map_results.png")

# # Post tweet with image
# tweet = "sample map"
# latitude = 51.484463
# longitude = -0.195405
# place_id = 'UK'
# post_result = api.update_status(status=tweet, media_ids=[media.media_id], lat=latitude, long=longitude)

if __name__ == "__main__":
    get_trending("United States")