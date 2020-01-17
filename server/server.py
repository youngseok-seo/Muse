from flask import Flask, jsonify, request, make_response, abort
from flask_cors import CORS

import sys
import os
import h5py
import csv
import numpy as np

csv.field_size_limit(1000000)

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json

sys.path.insert(0, 'ML')

app = Flask(__name__)
CORS(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.route('/', methods=['POST'])
def send_text():

    artist = request.json['artist']
    temp = request.json['temp']
    word = request.json['word']

    filename = get_filename(artist)
    filepath = f"ML/{filename}.h5"
    model = load_model(filepath)

    text = generate_text(model=model,
                         artist=artist,
                         temp=temp,
                         start_string=word)

    print(word)

    return make_response(jsonify(text=text), 201)

def get_filename(name):

    artists = {
        "ABBA": 'abba',
        "The Beatles": 'beatles',
        "Bee Gees": 'beegees',
        "Bon Jovi": 'bonjovi',
        "Elton John": 'eltonjohn',
        "Michael Jackson": 'michaeljackson',
        "Queen": 'queen',
        "Stevie Wonder": 'steviewonder'
    }

    return artists[name]

def generate_text(model, artist, temp, start_string):

    lyrics = []
    with open('ML/lyrics.csv') as csvfile:
        r = csv.reader(csvfile)
        for i, line in enumerate(r):
            if line[0] == artist:
                lyrics += line[1]

    vocab = sorted(set(lyrics))

    char_to_idx = {char:idx for idx, char in enumerate(vocab)}
    idx_to_char = np.array(vocab)

    # Number of characters to generate
    num_generate = 1000

    # Converting our start string to numbers (vectorizing)
    input_eval = [char_to_idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = temp

    # Here batch size == 1
    model.reset_states()
    for i in range(num_generate):
        predictions = model(input_eval)
        # remove the batch dimension
        predictions = tf.squeeze(predictions, 0)

        # using a categorical distribution to predict the word returned by the model
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        # We pass the predicted word as the next input to the model
        # along with the previous hidden state
        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(idx_to_char[predicted_id])

    return (start_string + ''.join(text_generated))


if __name__ == '__main__':
    app.run(port=5000, debug=True)