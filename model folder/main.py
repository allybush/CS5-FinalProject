import tensorflow as tf
import tensorflow.keras as keras

#import splitfolders

#splitfolders.ratio('C:/Users/sophi/PycharmProjects/dataset/new_music_data', output="C:/Users/sophi/PycharmProjects/MLMusic/", seed=1337, ratio=(.8, 0.2,0.0))

# preprocessing (finds it in the data directory)
train = tf.keras.preprocessing.image_dataset_from_directory("C:/Users/sophi/PycharmProjects/MLMusic/train", labels='inferred', label_mode='categorical', image_size=(231,348), color_mode="rgba", seed=0)

test = tf.keras.preprocessing.image_dataset_from_directory("C:/Users/sophi/PycharmProjects/MLMusic/val", labels='inferred', label_mode='categorical', image_size=(231,348), color_mode="rgba", seed=0)

# create model
model = tf.keras.models.Sequential()

# add model layers

model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(231, 348, 4)))
model.add(keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
model.add(keras.layers.BatchNormalization())

# 2nd conv layer
model.add(keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same'))
model.add(keras.layers.BatchNormalization())

# 3rd conv layer
model.add(keras.layers.Conv2D(32, (2, 2), activation='relu'))
model.add(keras.layers.MaxPooling2D((2, 2), strides=(2, 2), padding='same'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dropout(0.3))

# flatten output and feed it into dense layer
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation='relu'))

# output layer
model.add(keras.layers.Dense(8, activation='softmax'))

opt = tf.keras.optimizers.SGD(learning_rate=0.0001)

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.summary()
model.fit(train, validation_data=test, epochs=30)

model = model.save('C:/Users/sophi/PycharmProjects/MLMusic/model')
