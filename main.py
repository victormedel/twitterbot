from word_tweet_gen import get_trending, get_loc, map_generator, twitter_post




if __name__ == "__main__":
    trd_words = get_trending("United States")
    country, location, sugg_words = get_loc(trd_words)
    map_img = map_generator(str(location + ',' + country))
    twitter_post(country, location, trd_words, sugg_words)