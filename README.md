 <img src="project_logo.jpg">
 
 # Twitter sentiment analysis

This project aims to preprocess live tweets for further analysis. Steps involved:
* Raw data collecting
* Data preprocessing 
* Demographics prediction
* Category prediction
* Sentiment prediction

## Getting Started
### Prerequisites
```
emoji==0.5.4
Keras==2.3.1
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
tensorflow==1.15.0
Shapely==1.6.4.post1
torch>=1.0.0
numpy>=1.13
tqdm
Pillow
torchvision>=0.2.2
pycld2>=0.31
requests
pandas>=0.20
```
Also you need tweeter application  access keys that you define in listener.py 
You will need (consumer_key, consumer_secret, access_token, access_token_secret) [Link](https://developer.twitter.com/en/docs/basics/authentication/oauth-1-0a)

### Installing
* **m3inference package**
`pip install git+https://github.com/SlavOK400/m3inference.git`

* **twitter_sentiment package**
`git lfs install` then `git lfs clone https://github.com/SlavOK400/twitter_sentiment.git`

* **Define your twitter app keys:**
consumer_key, consumer_secret, access_token, access_token_secret in listener.py 

* **Mongo database.**
Please install the latest stable version and run MongoDB server. [Link](https://docs.mongodb.com/v3.2/administration/install-on-linux/)

## Usage
0. Go to `twitter_sentiment` directory on your machine
1. Run `listener.py` to start collecting tweets
2. Run `mongoexport --db tweets --collection training_tweets --out *.json`, where * is the name of your file, to convert collected tweets to a json file
3. Run `infer_demographics.py *.json`, where * is the name of your file, to predict demographics, categories and sentiment for your tweets. Input: json files. Output: single *_inferred.csv files

Originally all tweets from Canada will be collected, If you wish to change the location please update listener.py with:

`if "place" in datajson and datajson["place"]['country_code'] == "US":`
and
`stream.filter(locations=LOCATIONS_US )`

## Authors
*  [Slava Spirin](https://www.linkedin.com/in/slava-spirin/)
*  [Winston Li](https://www.linkedin.com/in/winstonl/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


