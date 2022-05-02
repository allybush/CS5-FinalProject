from sklearn.metrics import confusion_matrix
import keras
import numpy as np
import tensorflow as tf

datapath = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/smalldataset"

training = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.9, subset='training', seed=0)

test = tf.keras.preprocessing.image_dataset_from_directory(datapath, labels='inferred', label_mode='categorical', image_size=(288, 432), color_mode="rgba", validation_split=0.1, subset='validation', seed=0)

model = keras.models.load_model('/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model')


y_pred = model.predict(test) # TODO fix test so it's an array of (5,10) size

matrix = confusion_matrix(test, y_pred)
print(matrix.diagonal()/matrix.sum(axis=1))
