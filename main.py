import time
import threading
from datetime import datetime
from w3w_tweet import get_trending, get_loc, map_generator, twitter_post

WAIT_SECONDS = 43200

def twitter_post():
    # Establish current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Post to Twitter
    trd_words = get_trending("United States")
    sugg_words, nearest_loc, country, latitude, longitude = get_loc(trd_words)
    twitter_post(sugg_words, nearest_loc , country, latitude, longitude)

    print("Posted On = ", dt_string)


if __name__ == "__main__":
    
    ticker = threading.Event()
    while not ticker.wait(WAIT_SECONDS):
        twitter_post()
        