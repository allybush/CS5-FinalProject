"""

BEFORE USING: Set up a folder called "Data" and create 8 subfolders in that
folder called "classical", "country", "rap", "jazz", "metal", "pop",
"rock", or "indie" . Replace the first string in the variable "path" in line 67
with the absolute path of the bigger folder that holds the 7 subfolders. This should
fill each subfolder with images of the corresponding genre.

"""



import keras.preprocessing
import tensorflow as tf
import numpy as np
import requests


import json

import torch
from PIL import Image

import matplotlib.pyplot as plt

import librosa.display
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment

import io  # allows us to temporarily store the image to access with PIL

# mel spectrogram stuff

dst = 'test.wav'

#take stuff from spotipy

cid ='0d57547cb17c48aaa7aacd405a431360'
secret ='650f7983361f407eb6136da8d0010796'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

genres = ["classical","country","rap","jazz","metal","pop","rock"]


#arrays of playlist links
jazz = ["https://open.spotify.com/playlist/37i9dQZF1DWV7EzJMK2FUI?si=7890a79f446b4d3b", "https://open.spotify.com/playlist/37i9dQZF1DWW2c0C8Vb2IR?si=9a21e882cd574343", "https://open.spotify.com/playlist/37i9dQZF1DXbITWG1ZJKYt?si=500f86c4fe104aee", "https://open.spotify.com/playlist/37i9dQZF1DWSSSls9eK29h?si=c8f409839cab4507", "https://open.spotify.com/playlist/37i9dQZF1DX5S7hzwhDSyV?si=d9d73127dd564807", "https://open.spotify.com/playlist/37i9dQZF1DWSSSls9eK29h?si=261917c0d1854138", "https://open.spotify.com/playlist/37i9dQZF1DX6KyCRJzZneq?si=152d660dca1b417e", "https://open.spotify.com/playlist/37i9dQZF1DWTKezOYpetsD?si=72c5881a44f8434e", "https://open.spotify.com/playlist/37i9dQZF1DWV7EzJMK2FUI?si=5dc42fde6e7748f4"]
classical = ["https://open.spotify.com/playlist/37i9dQZF1DX2XWJkYVfE4v?si=8c0cd483a33b4324", "https://open.spotify.com/playlist/37i9dQZF1DX2XWJkYVfE4v?si=0c7b6e78c8984f56", "https://open.spotify.com/playlist/090o9Mrm7KaA3caCAIxb6A?si=307a3fea83334f33", "https://open.spotify.com/playlist/1h0CEZCm6IbFTbxThn6Xcs?si=b4378a85f1944228", "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0?si=eab76a4f7f344fa9", "https://open.spotify.com/playlist/090o9Mrm7KaA3caCAIxb6A?si=b156ee8adaa34f5d", "https://open.spotify.com/playlist/37i9dQZF1DX4s3V2rTswzO?si=33d990b70c424e77", "https://open.spotify.com/playlist/37i9dQZF1DWV0gynK7G6pD?si=fccbbdad495f4c8e"]
pop = ["https://open.spotify.com/playlist/37i9dQZF1DX2Nc3B70tvx0?si=4cdb3025465d48d0", "https://open.spotify.com/playlist/37i9dQZF1DXdbXrPNafg9d?si=1c13a3176f204868", "https://open.spotify.com/playlist/37i9dQZF1DX8uc99HoZBLU?si=2964a2daf528491b", "https://open.spotify.com/playlist/37i9dQZF1DX59NCqCqJtoH?si=115c77c8a4f54e54", "https://open.spotify.com/playlist/37i9dQZF1DXdTCdwCKzXwo?si=d59f0b71a1e64a51", "https://open.spotify.com/playlist/37i9dQZF1DXa2PvUpywmrr?si=f30b7d866f1a4516", "https://open.spotify.com/playlist/37i9dQZF1DWXti3N4Wp5xy?si=c47f20d30fac427f", "https://open.spotify.com/playlist/37i9dQZF1DX0MLFaUdXnjA?si=073635a5f5574131", "https://open.spotify.com/playlist/37i9dQZF1DX0kbJZpiYdZl?si=b2abd92458414c2f", "https://open.spotify.com/playlist/37i9dQZF1DWSPMbB1kcXmo?si=60ff2ee81c4841cd"]
metal = ["https://open.spotify.com/playlist/27gN69ebwiJRtXEboL12Ih?si=b3c058dbc3b141b8", "https://open.spotify.com/playlist/37i9dQZF1DX9qNs32fujYe?si=14b0eb029f964a88", "https://open.spotify.com/playlist/37i9dQZF1EQpgT26jgbgRI?si=61d60cc1ab344f87", "https://open.spotify.com/playlist/37i9dQZF1DWXNFSTtym834?si=c577fbf0587e490d", "https://open.spotify.com/playlist/37i9dQZF1DX5J7FIl4q56G?si=f7e6574a2f0147e6", "https://open.spotify.com/playlist/37i9dQZF1DWWOaP4H0w5b0?si=898c0e63481c4081", "https://open.spotify.com/playlist/37i9dQZF1DX2LTcinqsO68?si=720fd2e7757c4bfd"]
rap = ["https://open.spotify.com/playlist/0DoorcbBIsa7J6NW9FlLio?si=d90cf9a48f694cea", "https://open.spotify.com/playlist/4riovLwMCrY3q0Cd4e0Sqp?si=374db058d82c4b7d", "https://open.spotify.com/playlist/37i9dQZF1DX97h7ftpNSYT?si=44b0217025954f1d", "https://open.spotify.com/playlist/37i9dQZF1DWY4xHQp97fN6?si=3ace1db30b914d01", "https://open.spotify.com/playlist/37i9dQZF1DWVA1Gq4XHa6U?si=7c6fc9f3f6b44081", "https://open.spotify.com/playlist/37i9dQZF1DX0HRj9P7NxeE?si=b5b337f724884eda", "https://open.spotify.com/playlist/37i9dQZF1DX0Tkc6ltcBfU?si=30fe6fe369fa46be", "https://open.spotify.com/playlist/37i9dQZF1DWSUur0QPPsOn?si=64b939c527684d5e"]
rock = ["https://open.spotify.com/playlist/33VgmASznZ4gmwNrbhkD9m?si=a6df751c3fa44a1a", "https://open.spotify.com/playlist/5BygwTQ3OrbiwVsQhXFHMz?si=fa9e7af2aaae4418", "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=023caccfca29443d", "https://open.spotify.com/playlist/37i9dQZF1DWWGFQLoP9qlv?si=f16110e55b3240c5", "https://open.spotify.com/playlist/37i9dQZF1DX9wa6XirBPv8?si=835b6b946d7a4508", "https://open.spotify.com/playlist/37i9dQZF1DX82Zzp6AKx64?si=acb684bb917f4298"]
country = ["https://open.spotify.com/playlist/37i9dQZF1DX13kFuGnInkY?si=c98e787527c94a9b", "https://open.spotify.com/playlist/37i9dQZF1DWXepGEFFmQXJ?si=b3a1da3058e944f1", "https://open.spotify.com/playlist/37i9dQZF1DWYnwbYQ5HnZU?si=a5c0fed12bb7438a", "https://open.spotify.com/playlist/37i9dQZF1EQmPV0vrce2QZ?si=240d75254aa54ea2", "https://open.spotify.com/playlist/37i9dQZF1DX1lVhptIYRda?si=e474d00183764905", "https://open.spotify.com/playlist/37i9dQZF1DXdxUH6sNtcDe?si=69b089c9899d4811", "https://open.spotify.com/playlist/37i9dQZF1DWVFzWmxRnRJH?si=1c90eb52e02245c7"]


genresplaylist = [classical, country, rap, jazz, metal, pop, rock]


for y in range(len(genresplaylist)):
    count = 0
    for x in range(len(genresplaylist[y])):
        playlistname = genresplaylist[y][x]
        playlistresults = sp.playlist(playlistname)
        length = len(playlistresults['tracks']['items'])
        for z in range(length):
            path = "/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/newdata" + "/" + genres[y] + "/" + genres[y]
            try:
                songurl = playlistresults['tracks']['items'][z]['track']['preview_url']
                if songurl != None:

                    response = requests.get(songurl)
                    open("temp.mp3", "wb").write(response.content)

                    #### mel spectrogram section ####

                    # https://pythonbasics.org/convert-mp3-to-wav/
                    sound = AudioSegment.from_file("temp.mp3")
                    sound.export(dst, format="wav", bitrate="16k")

                    path = path + str(count) + ".png"
                    count += 1
                    print(path)

                    # trimming section
                    # thanks to this person https://stackoverflow.com/questions/56719138/how-can-i-save-a-librosa-spectrogram-plot-as-a-specific-sized-image

                    x, sr = librosa.load(dst, sr=1600)

                    # test if the file is longer than 30 seconds—if not, then it won't be consistent w training data.

                    duration = len(x) / sr

                    if duration > 29:
                        x, _ = librosa.effects.trim(x)
                        x = x[0:30 * sr]
                        x = x[0:431 * 512]

                        # convert to spectrogram section

                        spect = librosa.feature.melspectrogram(x, sr=sr, n_fft=1024, n_mels=288, hop_length=512)
                        S_dB = librosa.power_to_db(spect, ref=np.max)

                        # saving as an image of 432 x 288 dimensions

                        plt.figure(figsize=(4.5, 3))
                        plt.axis('off')
                        img = librosa.display.specshow(S_dB, n_fft=1024, hop_length=512)

                        # https://www.tutorialspoint.com/how-to-convert-matplotlib-figure-to-pil-image-object

                        plt.savefig(path, format='png', bbox_inches='tight', pad_inches=0)
                        img = Image.open(path)
                        img = img.convert("RGB")
                        img.save(path)


            except TypeError:
                print("eheheh")
