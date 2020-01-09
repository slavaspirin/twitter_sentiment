# Twitter sentiment analysis
Collects and predicts demographics of tweets

## Install
### m3inference
`pip install git+https://github.com/SlavOK400/m3inference.git`

### twitter_sentiment
`git clone https://github.com/SlavOK400/twitter_sentiment.git`

### mongo database
Please install the latest stable version and run MongoDB server. https://docs.mongodb.com/v3.2/administration/install-on-linux/

## Usage
0. Go to `twitter_sentiment` directory on your machine
1. Run `listener.py` to collect tweets
2. Run `mongoexport --db tweets --collection training_tweets --out *.json`, where * is the name of your file, to convert collected tweets to a json file
3. Run `infer_demographics.py *.json`, where * is the name of your file, to predict demographics, categories and sentiment for your tweets. Input: json files. Output: single *_inferred.csv files



and create a .CSV file with merged tweets and demographics


## Usefull datasets:
https://github.com/shaypal5/awesome-twitter-data#twitter-datasets
