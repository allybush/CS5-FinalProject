import matplotlib as plt
import librosa
import librosa.display
from pydub import AudioSegment
# files                                                                         
src = '/Users/allison/OneDrive/Allison/sysorecordings_term1/movement_2.mp3' #replace with any file you want :D
dst = 'test.wav' #keep this one the same

# convert wav to mp3                                                            
sound = AudioSegment.from_file(src)
sound.export(dst, format="wav", bitrate="16k")

audio_data = dst
x , sr = librosa.load(audio_data,sr=1600)

X = librosa.stft(x)
X= librosa.hz_to_mel(X,htk=False)
Xdb = librosa.amplitude_to_db(abs(X))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='log')
plt.pyplot.colorbar()
