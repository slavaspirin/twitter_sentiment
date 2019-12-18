# ! /home/slavok400/anaconda3/bin/python

from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import json

FOLDER = 'models'

def predict_sentiment(texts, batch_size=512):
    """
    :param texts: these texts should be preprocessed with re and emoticons replacements
    :param batch_size: default 512
    :return: numpy array of probabilities of shape (x,1)
    """

    # load model
    model = tf.keras.models.load_model(FOLDER + '/' + 'twitter_se_model.h5')

    with open(FOLDER + '/' + 'twitter_se_model_tokens.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    tokenized = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(tokenized, maxlen=350)
    return model.predict(padded, batch_size=batch_size, verbose=1).reshape(-1)


def predict_category(texts, batch_size=512):
    """
    :param texts: these texts should be preprocessed with re and emoticons replacements
    :param batch_size: default 512
    :return: numpy array of probabilities of shape (x,1)
    """

    model = tf.keras.models.load_model(FOLDER + '/' + 'reddit_model_v2.h5')

    with open(FOLDER + '/' + 'reddit_cat_model_tokens.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    categories = ['business', 'entertainment&arts', 'finance&economics', 'fun',
                  'health', 'politics', 'science&tech', 'sports']

    def decode_categories(predictions, input_categories):
        results = []
        for prediction in predictions:
            results.append(input_categories[prediction.argmax()])
        return results

    tokenized = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(tokenized, maxlen=350)
    raw_predictions = model.predict(padded, batch_size=batch_size, verbose=1)
    return decode_categories(raw_predictions, categories)
