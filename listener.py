#! /usr/bin/python
import tweepy
import pandas as pd
import json
import datetime
import pytz
from pymongo import MongoClient


auth = tweepy.OAuthHandler(consumer_key = 'b2naZOAwQBhBEHYFt2enZ660c',
                           consumer_secret = '3nUqbx6qMkVAIm0mV5bFnOhRZa1KCEQbbfWpzBWr1e5B2FPKyc')
auth.set_access_token('2465447359-nge8h5d3WTxZQZ3msNqTPHnqM0LAkwXOR6mQOPA',
                      'VS8W739mDtT9qdaK62iIEIRCLIP5YpBFUWzcotqWpdmkg')
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")




client = MongoClient('localhost', 27017)
count = 0
eastern = pytz.timezone('US/Eastern')

class StreamListener(tweepy.StreamListener):
    """tweepy.StreamListener is a class provided by tweepy used to access
    the Twitter Streaming API to collect tweets in real-time.

    Links:
    https://github.com/shawn-terryah/Twitter_Geolocation
    https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py#L118
    """
    def on_connect(self):
        """Called when the connection is made"""
        print("You're connected to the streaming server.")

    def on_error(self, status_code):
        """This is called when an error occurs"""
        if status_code == 420:
            return False

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        global count
        client = MongoClient()
        # store the results in training_tweets collection of tweets db
        db = client.tweets
        collection = db.training_tweets
        # decode JSON
        datajson = json.loads(data)
        # storying only tweets in English
        if "lang" in datajson and datajson["lang"] == "en":
            collection.insert_one(datajson)
        count += 1
        # print the progress every 1000 tweets
        ON_time = datetime.datetime.now(eastern)
        if count % 1000 == 0: print(count, ON_time.strftime('%a %b %d %Y %H:%M:%S'))

#         def on_status(self, status):
#         """This is called to check tweet's status.
#         Return nothing if was retweeted"""
#         if status.retweeted_status:
#             return



if __name__ == "__main__":

    LOCATIONS_US = [-124.7771694, 24.520833, -66.947028, 49.384472,        # Contiguous US
                     -164.639405, 58.806859, -144.152365, 71.76871,         # Alaska
                     -160.161542, 18.776344, -154.641396, 22.878623]

    LOCATIONS_CA = [-140.99778, 41.6751050889, -52.6480987209, 83.23324]    # Canada

    stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    stream = tweepy.Stream(auth, stream_listener)

    def run_listener():
        """Run listener. Wait and restart on error"""
        try:
            api = tweepy.API(auth)
            stream.filter(locations=LOCATIONS_CA) # locations=LOCATIONS OR track=['trump']
        except:
            time.sleep(5 * 60)
            run_listener()

    run_listener()