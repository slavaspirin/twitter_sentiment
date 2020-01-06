#! /usr/bin/python3
import tweepy
import json
import os
import datetime
import pytz
from pymongo import MongoClient
from m3inference import M3Twitter
import time

# set up API keys
auth = tweepy.OAuthHandler(consumer_key='b2naZOAwQBhBEHYFt2enZ660c',
                           consumer_secret='3nUqbx6qMkVAIm0mV5bFnOhRZa1KCEQbbfWpzBWr1e5B2FPKyc')
auth.set_access_token('2465447359-nge8h5d3WTxZQZ3msNqTPHnqM0LAkwXOR6mQOPA',
                      'VS8W739mDtT9qdaK62iIEIRCLIP5YpBFUWzcotqWpdmkg')
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# count and timezone
count = 0
eastern = pytz.timezone('US/Eastern')

# create cache folder and set up m3
if not os.path.exists('twitter_cache'):
    os.makedirs('twitter_cache')
m3twitter = M3Twitter(cache_dir="twitter_cache")


# create listener
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

        if "place" in datajson and datajson["place"]['country_code'] == "CA":

            m3_json = m3twitter.transform_jsonl_object(datajson)

            # M3 PROVIDED:
            # description
            # id
            # img_path
            # lang
            # name
            # screen_name

            if 'extended_tweet' in datajson:
                text = datajson['extended_tweet']['full_text']
            else:
                text = datajson['text']
            # text = text.replace('\n', '').replace(';', '')

            if datajson['coordinates']:
                coordinates_type = datajson['coordinates']['type']
                coordinates = datajson['coordinates']['coordinates']

            else:
                coordinates_type = datajson['place']['bounding_box']['type']
                coordinates = datajson['place']['bounding_box']['coordinates']

                # use more detailed area if available
            if datajson['place']['place_type'] == 'admin':
                place = datajson['place']['name']
            else:
                place = datajson['place']['full_name']

            m3_json['created_at'] = datajson['created_at']
            m3_json['text'] = text
            m3_json['utc_offset'] = datajson['user']['utc_offset']
            m3_json['profile_location'] = datajson['user']['location']
            m3_json['followers_count'] = datajson['user']['followers_count']
            m3_json['friends_count'] = datajson['user']['friends_count']
            m3_json['favourites_count'] = datajson['user']['favourites_count']
            m3_json['statuses_count'] = datajson['user']['statuses_count']
            m3_json['listed_count'] = datajson['user']['listed_count']
            m3_json['coordinates_type'] = coordinates_type
            m3_json['coordinates'] = coordinates
            m3_json['place'] = place
            m3_json['country_code'] = datajson['place']['country_code']
            # m3_json['pic_address'] = datajson['user']["profile_image_url_https"]

            collection.insert_one(m3_json)

            count += 1
            # print the progress every 1000 tweets
            on_time = datetime.datetime.now(eastern)
            if count % 1000 == 0:
                print(count, on_time.strftime('%a %b %d %Y %H:%M:%S'))


#         def on_status(self, status):
#         """This is called to check tweet's status.
#         Return nothing if was retweeted"""
#         if status.retweeted_status:
#             return


if __name__ == "__main__":

    LOCATIONS_US = [-124.7771694, 24.520833, -66.947028, 49.384472,  # Contiguous US
                    -164.639405, 58.806859, -144.152365, 71.76871,  # Alaska
                    -160.161542, 18.776344, -154.641396, 22.878623]

    LOCATIONS_CA = [-140.99778, 41.6751050889, -52.6480987209, 83.23324]  # Canada

    stream_listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))
    stream = tweepy.Stream(auth, stream_listener)


    stream.filter(locations=LOCATIONS_CA)  # locations=LOCATIONS OR track=['trump']
