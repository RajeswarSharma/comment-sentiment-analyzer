
from flask import Flask, render_template, request, jsonify
from flask.helpers import get_root_path
import keras.models
import os
import sys
import json
import helpers
import pandas as pd
import numpy as np
sys.path.append(os.path.abspath("tweet_sentiment_extraction.h5"))

# init flask

app = Flask(__name__)


@app.route('/')
def index():
    return "hello there"


@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = request.get_json()
    # print(type(json_data))
    path = "C:/Users/Rajeswar Sharma/Documents/minor project 2/comment-sentiment-analyzer/classifier/raw.json"
    # with open(path, encoding="utf-8") as json_file:
    #     data = json.load(json_file)
    # #data = json.loads(json_data)
    #data = helpers.limit_text(data)

    df = pd.DataFrame(data, columns=["text"])
    df["text"] = df["text"].apply(helpers.normalization)
    df['word_count'] = df['text'].apply(helpers.word_count)
    df.text = df.text.astype(str)
    tk = helpers.tk
    tk.fit_on_texts(df.text.values)

    X_text_indices = tk.texts_to_sequences(df.text.values)
    X_text_indices = helpers.sequence.pad_sequences(X_text_indices, maxlen=31)

    result = helpers.model.predict(X_text_indices)

    for i in range(len(result)):
        result[i] = np.argmax(result[i])
    res = result[1:, 0]

    output = np.array(list(map(helpers.mapper, res)))
    number_list = np.array(output)
    (unique, counts) = np.unique(number_list, return_counts=True)
    
    response = {
        "total":len(output),
        "sentiments":unique.tolist(),
        "counts":counts.tolist()
    }
    print(response)
    response_json = json.dumps(response)
    return response_json


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
