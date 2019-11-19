#! /usr/bin/python3

import os.path
import json
from m3inference.dataset import TW_DEFAULT_PROFILE_IMG
from PIL import Image

tweets = []
missing_pics = 0
wrong_sized = []
count = 0

for line in open('training_tweets.json', encoding="utf8").readlines():
    loads = json.loads(line)
    tweets.append(loads)

    if not os.path.exists(loads['img_path']):
        loads['img_path'] = TW_DEFAULT_PROFILE_IMG
        missing_pics += 1

    image = Image.open(loads['img_path'])
    if not image.size == (224, 224):
        wrong_sized.append(count)

    count += 1
print("{} missing profile images with {} wrong sizes".format(missing_pics, len(wrong_sized)))
