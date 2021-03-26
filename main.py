import time
import threading
from w3w_tweet import get_trending, get_loc, map_generator, twitter_post

WAIT_SECONDS = 43200

def twitter_post():
    trd_words = get_trending("United States")
    sugg_words, nearest_loc, country, latitude, longitude = get_loc(trd_words)
    twitter_post(sugg_words, nearest_loc , country, latitude, longitude)


if __name__ == "__main__":
    
    ticker = threading.Event()
    while not ticker.wait(WAIT_SECONDS):
        twitter_post()
        