import tweepy
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Authenticate to Twitter
auth = tweepy.OAuthHandler(cfg['twitter_auth']['api_key'], cfg['twitter_auth']['api_secret_key'])
auth.set_access_token(cfg['twitter_auth']['access_token'], cfg['twitter_auth']['secrete_access_token'])

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# API Authentication Check
try:
    api.verify_credentials()
    print("Authentication OK")

except Exception:
    print("Error during authentication")

# Upload image
media = api.media_upload("map_results.png")

# Post tweet with image
tweet = "sample map"
latitude = 51.484463
longitude = -0.195405
place_id = 'UK'
post_result = api.update_status(status=tweet, media_ids=[media.media_id], lat=latitude, long=longitude)

