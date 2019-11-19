#! /usr/bin/python3

import json
from m3inference import M3Twitter

tweets = [json.loads(line) for line in open('training_tweets.json', encoding="utf8").readlines()]

m3twitter = M3Twitter(cache_dir="twitter_cache")
demographics = m3twitter.infer(tweets, batch_size=30, num_workers=4)





