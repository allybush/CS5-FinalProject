import tensorflow as tf
import numpy as np
import cv2
genres = np.array(["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"])

# preprocessing (finds it in the data directory)
training = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels ='inferred', label_mode='categorical', validation_split=0.9, subset='training', seed=10)


test = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels ='inferred', label_mode='categorical', validation_split=0.1, subset='validation', seed=10)


# create model
model = tf.keras.models.Sequential()
# add model layers
model.add(tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', input_shape=(256, 256, 3)))
model.add(tf.keras.layers.Conv2D(32, kernel_size=3, activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(training, validation_data=(test), epochs=5)

