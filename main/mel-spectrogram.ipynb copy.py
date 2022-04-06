import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
import numpy as np
# files                                                                         
src = '/Users/allison/OneDrive - BushChang Corporation/Allison/school/11th grade/cs/kerasstuff/Data/recording.m4a' #replace with any file you want :D
dst = 'test.wav' #keep this one the same

# convert format to mp3
sound = AudioSegment.from_file(src)
sound.export(dst, format="wav", bitrate="16k")

audio_data = dst

x, sr = librosa.load(audio_data, sr=1600)
x, _ = librosa.effects.trim(x)

spect = librosa.feature.melspectrogram(y=x, sr=sr)

fig, ax = plt.subplots()
S_dB = librosa.power_to_db(spect, ref=np.max)
img = librosa.display.specshow(S_dB, sr=sr, ax=ax)
plt.show()
plt.savefig(img, format='png')



