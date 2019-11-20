# twitter_sentiment
Collects and predicts demographics of tweets

## Install
### m3inference
`pip install git+https://github.com/SlavOK400/m3inference.git`

### twitter_sentiment
`git clone https://github.com/SlavOK400/twitter_sentiment.git`

## Usage
1. Run `listener.py` to collect tweets
2. Run `mongoexport --db tweets --collection training_tweets --out training_tweets.json` to convert collected tweets to a json file
3. Run `infer_demographics.py` to predict demographocs and create a .CSV file with merged tweets and demographics


## Usefull datasets:
https://github.com/shaypal5/awesome-twitter-data#twitter-datasets
