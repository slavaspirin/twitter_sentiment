#! /usr/bin/python3

import os.path
import json
from m3inference import M3Twitter
from m3inference.dataset import TW_DEFAULT_PROFILE_IMG


cache_path = "twitter_cache"
tweets = []
missing_pics = 0

count = 0
for line in open('training_tweets.json', encoding="utf8").readlines():
    loads = json.loads(line)
    tweets.append(loads)

    if count > 200:
        break

    if not os.path.exists(loads['img_path']):
        loads['img_path'] = TW_DEFAULT_PROFILE_IMG
        missing_pics += 1

print("{} missing profile images".format(missing_pics))

m3twitter = M3Twitter(cache_dir=cache_path)
demographics = m3twitter.infer(tweets, batch_size=30, num_workers=4)

get_demog = lambda k: {k: (max(v, key=v.get)) for (k, v) in k.items()}

for tweet in tweets:
    tweet.update(get_demog(demographics[tweet['id']]))

with open('tweets&demographics.json', 'w', encoding="utf8") as f:
    for tweet in tweets:
        f.write(json.dumps(tweet))
