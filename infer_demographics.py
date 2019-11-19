#! /usr/bin/python3

import os.path
import json
from m3inference import M3Twitter
from m3inference.dataset import TW_DEFAULT_PROFILE_IMG
import csv

# tweets = [json.loads(line) for line in open('training_tweets.json', encoding="utf8").readlines()]

tweets = []
missing_pics = 0


# create a list of dictionaries(tweets), replace missing images with default ones
for line in open('training_tweets.json', encoding="utf8").readlines():
    loads = json.loads(line)
    tweets.append(loads)

    if not os.path.exists(loads['img_path']):
        loads['img_path'] = TW_DEFAULT_PROFILE_IMG
        missing_pics += 1
print("{} missing profile images".format(missing_pics))


# predict demographics
m3twitter = M3Twitter(cache_dir="twitter_cache")
demographics = m3twitter.infer(tweets, batch_size=50, num_workers=4)

# create a function to return the keys with max probabilities
get_demog = lambda k: {k: (max(v, key=v.get)) for (k, v) in k.items()}

# create and write a csv file
with open("tweets_and_demographics.csv", "w") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    # write first row with keys
    writer.writerow(tweets[0].keys())
    for tweet in tweets:
        # add demographics to tweets
        tweet.update(get_demog(demographics[tweet['id']]))
        # edit text to make it readable. \n is used for new line for csv interpreters
        tweet['text'] = tweet['text'].replace('\n', ' ')
        row = tweet.values()
        writer.writerow(row)
