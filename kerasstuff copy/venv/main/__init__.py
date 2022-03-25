import tensorflow as tf
import numpy as np



genres = np.array(["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"])

# preprocessing (finds it in the data directory)
training = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels ='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.9, subset='training', seed=10)


test = tf.keras.preprocessing.image_dataset_from_directory("/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original", labels ='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.1, subset='validation', seed=10)


# create model
model = tf.keras.models.Sequential()
# add model layers


model.add(tf.keras.layers.Conv2D(60, kernel_size=8, activation='relu', input_shape=(288, 432, 4)))
model.add(tf.keras.layers.Conv2D(30, kernel_size=5, activation='relu'))
model.add(tf.keras.layers.Conv2D(10, kernel_size=5, activation='relu'))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(3, activation='relu'))
model.add(tf.keras.layers.Dense(5, activation='relu'))
model.add(tf.keras.layers.Dense(3, activation='relu'))
model.add(tf.keras.layers.Dense(5, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='relu'))


model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(training, validation_data=test, epochs=7)

model = model.save('/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model')






