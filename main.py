from word_tweet_gen import get_trending, get_loc, map_generator, twitter_post




if __name__ == "__main__":
    
    trd_words = get_trending("United States")
    sugg_words, nearest_loc, country, latitude, longitude = get_loc(trd_words)
    map_img = map_generator(str(nearest_loc + ',' + country))
    twitter_post(sugg_words, nearest_loc , country, latitude, longitude)