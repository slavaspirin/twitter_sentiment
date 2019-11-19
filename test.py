#! /usr/bin/python3

from m3inference.dataset import TW_DEFAULT_PROFILE_IMG
import os.path
import json
from m3inference import M3Twitter
from PIL import Image

tweets = []
missing_pics = 0
wrong_sized = []
count = 0

# for line in open('training_tweets.json', encoding="utf8").readlines():
#     loads = json.loads(line)
#     tweets.append(loads)
#
#     if not os.path.exists(loads['img_path']):
#         loads['img_path'] = TW_DEFAULT_PROFILE_IMG
#         missing_pics += 1
#
#     image = Image.open(loads['img_path'])
#     if not image.size == (224, 224):
#         wrong_sized.append(count)
#
#     count += 1
# print("{} missing profile images with {} wrong sizes".format(missing_pics, len(wrong_sized)))

# create a list of dictionaries(tweets), replace missing images with default ones
for line in open('training_tweets.json', encoding="utf8").readlines():

    if (count > 441 * 50) and (count < 444 * 50):  # REMOVE
        loads = json.loads(line)
        tweets.append(loads)

        if not os.path.exists(loads['img_path']):
            loads['img_path'] = TW_DEFAULT_PROFILE_IMG
            missing_pics += 1

    count += 1  # REMOVE

print(count)

# predict demographics
m3twitter = M3Twitter(cache_dir="twitter_cache")
demographics = m3twitter.infer(tweets, batch_size=50, num_workers=4)
