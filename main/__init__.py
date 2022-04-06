import tensorflow as tf
from tensorflow.keras.layers import LeakyReLU
import numpy as np
from PIL import Image

# preprocessing (finds it in the data directory)
training = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.9, subset='training', seed=0)

test = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.1, subset='validation', seed=0)

# create model
model = tf.keras.models.Sequential()

# add model layers

model.add(tf.keras.layers.Conv2D(64, kernel_size=4, strides=3, input_shape=(288, 432, 4)))
model.add(tf.keras.layers.Conv2D(64, kernel_size=5, strides=5))
model.add(tf.keras.layers.Conv2D(64, kernel_size=6, strides=6))
model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dense(20))
model.add(tf.keras.layers.Dense(20))
model.add(tf.keras.layers.Dropout(rate=0.05))

model.add(tf.keras.layers.Dense(20))
model.add(tf.keras.layers.Dense(20))

model.add(tf.keras.layers.Dense(10, activation='softmax'))


opt = tf.keras.optimizers.Adam(learning_rate=0.01)

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(training, validation_data=test, epochs=100)

model = model.save('/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model')
