import keras.models
import keras.preprocessing
import tensorflow as tf
import numpy as np


import torch
from PIL import Image
import torchvision.transforms as transforms

genres = np.array(["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"])

filename = '/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/images_original/reggae/reggae00001.png'
model = keras.models.load_model('/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/model')
#thanks to this dude for helping with converting an image to a tensor https://www.tutorialspoint.com/how-to-convert-an-image-to-a-pytorch-tensor


image = Image.open(filename)


image = tf.convert_to_tensor(image, dtype=tf.float32)
image = np.array([image])

##Convert single image to a batch.

predictions = model.predict(image)
predictions = np.argmax(predictions)
predictions = genres[predictions]

print(predictions)
