import tensorflow as tf
import numpy as np
from PIL import Image


savemodelpath = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model"

datapath = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/newdata"

# preprocessing (finds it in the data directory)
training = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(231,348), color_mode="rgba", validation_split=0.9, subset='training', seed=0)

test = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(231, 348), color_mode="rgba", validation_split=0.1, subset='validation', seed=0)

# create model
model = tf.keras.models.Sequential()

# add model layers

## model.add(tf.keras.layers.Conv2D(64, kernel_size=4, strides=3, input_shape=(288, 432, 4)))
## model.add(tf.keras.layers.Conv2D(64, kernel_size=6, strides=5))

model.add(tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(231, 348, 4)))
model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2)))
model.add(tf.keras.layers.BatchNormalization())

model.add(tf.keras.layers.Conv2D(32, 4, activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2)))
model.add(tf.keras.layers.BatchNormalization())

model.add(tf.keras.layers.Flatten())

model.add(tf.keras.layers.Dropout(rate=0.7))

model.add(tf.keras.layers.Dense(30, activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=1e-5, l2=1e-4)))
model.add(tf.keras.layers.Dropout(rate=0.5))
model.add(tf.keras.layers.Dense(30, activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=1e-5, l2=1e-4)))

#also maybe add cross-validation

model.add(tf.keras.layers.Dense(7, activation='softmax'))


opt = tf.keras.optimizers.SGD(learning_rate=0.0001) #SGD results in more generalization than ADAM, which makes sense with music genres.

model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['categorical_accuracy'])

#ty to this person for confusion matrix help: https://stackoverflow.com/questions/39770376/scikit-learn-get-accuracy-scores-for-each-class

model.fit(training, validation_data=test, epochs=450)


model = model.save(savemodelpath)
