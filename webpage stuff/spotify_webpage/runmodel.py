import keras.models
import keras.preprocessing
import tensorflow as tf
import numpy as np
import requests

import torchvision

import torch
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import librosa
import librosa.display

from pydub import AudioSegment

import io  # allows us to temporarily store the image to access with PIL

def run(path):
    # files
    response = requests.get(path)
    open("temp.mp3", "wb").write(response.content)

    src = "temp.mp3" #replace with any file you want :D

    dst = 'test.wav'
    # convert format to mp3

    # https://pythonbasics.org/convert-mp3-to-wav/

    sound = AudioSegment.from_file(src)
    sound.export(dst, format="wav", bitrate="16k")

    #trimming section

    # thanks to this person https://stackoverflow.com/questions/56719138/how-can-i-save-a-librosa-spectrogram-plot-as-a-specific-sized-image

    x, sr = librosa.load(dst, sr=1600)

    #test if the file is longer than 30 seconds—if not, then it won't be consistent w training data.

    duration = len(x)/sr

    if duration > 29:
        x, _ = librosa.effects.trim(x)
        x = x[0:30*sr]
        x = x[0:431*512]

        # convert to spectrogram section

        spect = librosa.feature.melspectrogram(x, sr=sr, n_mels=288, hop_length=512)
        S_dB = librosa.power_to_db(spect, ref=np.max)

        # saving as an image of 432 x 288 dimensions

        plt.figure(figsize=(4.5,3)) # idk why this size works but it does (even tho it doesn't follow the pixel to inches conversion)
        plt.axis('off')

        img = librosa.display.specshow(S_dB, hop_length=512)

        savedimage = io.BytesIO()

        # https://www.tutorialspoint.com/how-to-convert-matplotlib-figure-to-pil-image-object

        plt.savefig(savedimage, format='png', bbox_inches='tight', pad_inches=0)

        # starting to run it on the model

        genres = np.array(["classical", "country", "rap", "jazz", "metal", "pop", "rock"])


        model = keras.models.load_model('model')
        # thanks to this dude for helping with converting an image to a tensor https://www.tutorialspoint.com/how-to-convert-an-image-to-a-pytorch-tensor

        image = Image.open(savedimage)
        image = image.convert('RGB')
        image = torchvision.transforms.functional.to_tensor(image)
        image = np.array(image)
        image = np.reshape(image,(1,231,348,3))

        # convert single image to a batch.

        predictions = model.predict(image)
        predictions = np.argmax(predictions)
        predictions = genres[predictions]

        # savedimage.close()
        return predictions
    else:
        print("Your clip is only " + str(duration) + " seconds. Make sure it's more than 30 seconds!")
        return "no"
