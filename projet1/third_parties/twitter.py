import os 
from datetime import datetime, timezone
import logging 
import tweepy
from dotenv import load_dotenv


load_dotenv()
access_token = os.environ.get("TWITTER_API_KEY")
access_token_secret = os.environ.get("TWITTER_API_KEY_SECRET")

logger = logging.getLogger("twitter")

auth = tweepy.OAuthHandler(
     access_token, access_token_secret

)

api = tweepy.API(auth)

