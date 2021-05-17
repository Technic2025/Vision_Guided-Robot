#This program trains a convolutional neural network to recognize images as either "blocked" or "open"

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import keras.losses

DATADIR = ""#Directory of training images
CATEGORIES = ["Blocked", "Open"]
IMG_SIZE = 65

training_data = []

for category in CATEGORIES:
    path = os.path.join(DATADIR, category)
    class_num = CATEGORIES.index(category)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
        img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        training_data.append([img_array, class_num])

random.shuffle(training_data)

x_train = []
y_train = []

for features, label in training_data:
    x_train.append(features)
    y_train.append(label)

x_train = np.array(x_train).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
y_train = np.array(y_train)

x_train = tf.keras.utils.normalize(x_train, axis = 1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(IMG_SIZE**2, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(100, activation = tf.nn.relu))
model.add(tf.keras.layers.Dense(2, activation = tf.nn.softmax))

model.compile(optimizer = "adam", loss = keras.losses.SparseCategoricalCrossentropy(), metrics = ["accuracy"])
model.fit(x_train, y_train, batch_size = 1, epochs = 5)

model.save("visionGuidedRobotNeuralNetwork.model")
