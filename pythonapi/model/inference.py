import os
import numpy as np
import tensorflow as tf
from PIL import Image
import pickle5 as pickle
from matplotlib import pyplot as plt

# matplotlib.use("TkAgg")
results = {}

with open('index_word.pkl', 'rb') as file:
    index_word = pickle.load(file)

with open('word_index.pkl', 'rb') as file:
    word_index = pickle.load(file)

# transformer = None
image_path = './Dataset/Flicker8k_Dataset/'
dir_Flickr_text = './Dataset/Flickr8k.token.txt'


def i_map_func(img_name, cap):
    img_tensor = np.load(img_name.decode('utf-8') + '.npy')
    return img_tensor, img_name, cap


def remove_list_extension(i):
    ret_val, *_ = i.split('.')
    return ret_val


def append_to_list(caption):

    output = []

    for i in caption[0]:
        output.append(index_word[i])

    return output


def create_padding_mask(seq):
    seq = tf.cast(tf.math.equal(seq, 0), tf.float32)
    return seq[:, tf.newaxis, tf.newaxis, :]


def create_look_ahead_mask(size):
    mask = 1 - tf.linalg.band_part(tf.ones((size, size)), -1, 0)
    return mask


def create_masks_decoder(tar):
    look_ahead_mask = create_look_ahead_mask(tf.shape(tar)[1])
    dec_target_padding_mask = create_padding_mask(tar)
    combined_mask = tf.maximum(dec_target_padding_mask, look_ahead_mask)
    return combined_mask


def evaluate(image, transformer):
    start_token = word_index["<start>"]
    end_token = word_index["<end>"]
    decoder_input = [start_token]
    decoder_input = np.repeat(decoder_input, repeats=1)
    output = tf.cast(tf.expand_dims(decoder_input, 1),
                     dtype=tf.int32)  # tokens

    for i in range(40):
        dec_mask = create_masks_decoder(output)
        predictions, attention_weights = transformer(
            image, output, False, dec_mask)
        predictions = predictions[:, -1:, :]  # (batch_size, 1, vocab_size)
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)
        if tf.math.equal(predicted_id, end_token):
            break
        output = tf.concat([output, predicted_id], axis=-1)

    output = append_to_list(output.numpy())
    f_cap = " ".join([f" {i}" for i in output])

    return f_cap
