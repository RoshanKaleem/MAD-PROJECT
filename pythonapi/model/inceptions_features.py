import os
import numpy as np
from tensorflow import keras
import tensorflow as tf


image_model = tf.keras.applications.InceptionV3(
    include_top=False,
    weights='imagenet'
)

new_input = image_model.input
hidden_layer = image_model.layers[-1].output
image_features_extract_model = tf.keras.Model(new_input, hidden_layer)


def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)

    img = tf.image.resize(img, (299, 299))
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    return img


def inception_features(file_pth, BATCH_SIZE=128):

    img = load_image(file_pth)
    _k = tf.expand_dims(img, 0)
    features = image_features_extract_model(_k)
    batch_features = tf.reshape(features, (64, 2048))
    return batch_features
