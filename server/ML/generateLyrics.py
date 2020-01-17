import tensorflow as tf
import pandas as pd
import numpy as np

import os
import time

import csv
csv.field_size_limit(1000000)

abba_lyrics = []
with open('lyrics.csv') as csvfile:
    r = csv.reader(csvfile)
    for i, line in enumerate(r):
        if i == 0:
            abba_lyrics = line[1]

vocab = sorted(set(abba_lyrics))

char_to_idx = {char:idx for idx, char in enumerate(vocab)}
idx_to_char = np.array(vocab)
int_text = np.array([char_to_idx[char] for char in abba_lyrics])

seq_length = 100
len_examples = len(abba_lyrics)
char_dataset = tf.data.Dataset.from_tensor_slices(int_text)

sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

# for item in sequences.take(2):
#     print(repr(''.join(idx_to_char[item.numpy()])))

def split_text(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_text)

# for input_example, target_example in dataset.take(1):
#     print ('Input data: ', repr(''.join(idx_to_char[input_example.numpy()])))
#     print ('Target data:', repr(''.join(idx_to_char[target_example.numpy()])))

# for i, (input_idx, target_idx) in enumerate(zip(input_example[:5], target_example[:5])):
#     print("Step {:4d}".format(i))
#     print("  input: {} ({:s})".format(input_idx, repr(idx_to_char[input_idx])))
#     print("  expected output: {} ({:s})".format(target_idx, repr(idx_to_char[target_idx])))

BATCH_SIZE = 64
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

# MODEL

vocab_size = len(vocab)
embedding_dim = 256
rnn_units = 1024

def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model =  tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, batch_input_shape=[batch_size, None]),
        tf.keras.layers.GRU(rnn_units, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    
    return model

model = build_model(vocab_size=vocab_size,
                    embedding_dim=embedding_dim,
                    rnn_units=rnn_units,
                    batch_size=BATCH_SIZE)

# model.summary()

for input_example_batch, target_example_batch in dataset.take(1):
    example_batch_predictions = model(input_example_batch)
    # print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")

sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
sampled_indices = tf.squeeze(sampled_indices,axis=-1).numpy()

# print('sampled indices: ', sampled_indices)

# print("Input: \n", repr("".join(idx_to_char[input_example_batch[0]])))
# print()
# print("Next Char Predictions: \n", repr("".join(idx_to_char[sampled_indices])))

def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

example_batch_loss  = loss(target_example_batch, example_batch_predictions)
# print("Prediction shape: ", example_batch_predictions.shape, " # (batch_size, sequence_length, vocab_size)")
# print("scalar_loss: ", example_batch_loss.numpy().mean())

model.compile(optimizer='adam', loss=loss)

# CHECKPOINTS

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")
checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix, save_weights_only=True)

# TRAIN

EPOCHS = 10

history = model.fit(dataset, epochs=EPOCHS)

# tf.train.latest_checkpoint(checkpoint_dir)

model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))

def generate_text(model, start_string):
    # Evaluation step (generating text using the learned model)

    # Number of characters to generate
    num_generate = 1000

    # Converting our start string to numbers (vectorizing)
    input_eval = [char2idx[s] for s in start_string]
    input_eval = tf.expand_dims(input_eval, 0)

    # Empty string to store our results
    text_generated = []

    # Low temperatures results in more predictable text.
    # Higher temperatures results in more surprising text.
    # Experiment to find the best setting.
    temperature = 0.1

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

        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))

print(generate_text(model, start_string=u"You are"))