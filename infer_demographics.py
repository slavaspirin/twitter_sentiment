#! /usr/bin/python3

import sys
import os.path
import json
from m3inference import M3Twitter
from m3inference.dataset import TW_DEFAULT_PROFILE_IMG
import csv
import emoji
import re
import infer_sentiment_and_category

# tweets = [json.loads(line) for line in open('training_tweets.json', encoding="utf8").readlines()]

arguments = sys.argv[1:]

# check if all files have .json extension
for argument in arguments:
    assert argument[-5:] == '.json', (
        'Error in infer_demographics: input file "%s" has to have .json extension' % argument)

for file in arguments:
    tweets = []
    missing_pics = 0

    # create a list of dictionaries(tweets), replace missing images with default ones
    for line in open(file, encoding="utf8").readlines():
        loads = json.loads(line)
        tweets.append(loads)

        if not os.path.exists(loads['img_path']):
            loads['img_path'] = TW_DEFAULT_PROFILE_IMG
            missing_pics += 1
    print("{} missing profile images".format(missing_pics))

    # predict demographics
    m3twitter = M3Twitter(cache_dir="twitter_cache")
    demographics = m3twitter.infer(tweets, batch_size=64, num_workers=1)
    # create a function to return the keys with max probabilities
    get_demog = lambda k: {k: (max(v, key=v.get)) for (k, v) in k.items()}


    def clean_str(string):
        """
        Tokenization/string cleaning for dataset
        """

        # lowercase
        string = string.lower()
        # replace urls
        string = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '<url>', string)
        string = re.sub(r'http\S+', '<url>', string)
        # remove html tags
        string = re.sub('<[^>]*>', ' ', string)
        string = string.replace('\n', ' ')
        # replace users
        string = re.sub('@[^\s]+', '<user>', string)
        # remove #
        string = re.sub(r'#([^\s]+)', r'\1', string)
        # replace emojis with their short names
        string = emoji.demojize(string)
        string = re.sub(r':([\w]+):', r' \1 ', string).replace('_', ' ')
        # strip spaces
        string = string.strip()
        return string


    # extract and clean texts, convert to list
    texts = [clean_str(tweet['text']) for tweet in tweets]
    # predict categories
    predicted_categories = infer_sentiment_and_category.predict_category(texts, 512)
    # predict sentiments
    predicted_sentiments = infer_sentiment_and_category.predict_sentiment(texts, 512)

    # create and write a csv file
    with open(file[:-5] + '_inferred.csv', "w", encoding="utf8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        # write first row with keys
        writer.writerow(list(tweets[0].keys()) + ['sex', 'age', 'org', 'sentiment', 'category'])
        for no, tweet in enumerate(tweets):
            # add demographics to tweets
            tweet.update(get_demog(demographics[tweet['id']]))
            tweet.update({'sentiment': predicted_sentiments[no]})
            tweet.update({'category': predicted_categories[no]})
            # edit text to make it readable. \n is used for new line for csv interpreters
            tweet['text'] = tweet['text'].replace('\n', ' ')
            row = tweet.values()
            writer.writerow(row)
