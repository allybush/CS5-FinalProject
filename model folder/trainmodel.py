"""
To use: change "datapath" in line 13 to the absolute path of the "Data" folder you downloaded or created in dataset.py (not the inner folders). Change "savemodelpath" in line
11 to the path of wherever you want the model to be. This path must be the same as the path used in model.load(path) in runmodel.py

"""
import tensorflow as tf
import numpy as np
from PIL import Image


savemodelpath = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model"

datapath = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/newdata"

# preprocessing (finds it in the data directory)
train = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(231,348), color_mode="rgb", validation_split=0.9, subset='training', seed=0)

test = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(231, 348), color_mode="rgb", validation_split=0.1, subset='validation', seed=0)

# create model
model = tf.keras.models.Sequential()

# add model layers
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(231, 348, 3)))
model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
model.add(tf.keras.layers.BatchNormalization())

 # 2nd conv layer
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
model.add(tf.keras.layers.BatchNormalization())

 # 3rd conv layer
model.add(tf.keras.layers.Conv2D(32, (2, 2), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2), strides=(2, 2), padding='same'))
model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(0.3))

 # flatten output and feed it into dense layer
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))

 # output layer
model.add(tf.keras.layers.Dense(7, activation='softmax'))

opt = tf.keras.optimizers.SGD(learning_rate=0.0001)

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(train, validation_data=test, epochs=30)


model = model.save(savemodelpath)
