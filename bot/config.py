#!/usr/bin/env python
# twitter-bot/bot/config.py
import os
import tweepy
import logging

logger = logging.getLogger()


def create_twitter_api():
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e

    logger.info("Twitter API created")
    return api


def create_google_api():
    logger.info("Google API created")
    g_api = os.getenv("GOOGLE_API_KEY")
    return g_api


def create_w3w_api():
    logger.info('W3W API created')
    w3w_api = os.getenv("W3W_API_KEY")
    return w3w_api
