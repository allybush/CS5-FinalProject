# CS5-FinalProject Instructions

## Set Up

1. Install Python 3.8-64 version or use any 3.8-3.9 version you already have installed. (https://www.python.org/downloads/release/python-380/)
2. Use an IDE of your choice (we used PyCharm) to open "model folder"
3. Configure the interpreter for Python 3.8 (the version you just installed) and install the necessary packages (keras, tensorflow, numpy, PIL, matplotlib, librosa, pydub, spotipy, ffmpeg, ffprobe). 
4. Create a folder anywhere on your computer titled "Data" with 7 subfolders titled "pop", "rock", "classical", "jazz", "metal", "country", and "rap"
5. Navigate to `dataset.py` and follow the instructions at the top.
6. Run `dataset.py`
7. At this point, you might encounter a WINERROR. To solve this, download ffmpeg from this link (https://ffmpeg.org/download.html) and ensure that the three files in the ffmpeg package (fmpeg.exe, ffprobe.exe, ffplay.exe) are located on your path so they can be run.
8. After running `dataset.py`, which should take roughly 2-3 hours (depending on your computer) navigate to `trainmodel.py`. (You should've ended up with a massive folder and 7 smaller folders of roughly 800 RGB images each).
10. Follow the instructions at the top of `trainmodel.py`
11. Run `trainmodel.py`
12. Navigate to webpage_stuff/spotify_webpage and locate `runmodel.py`
13. Follow the instructions at the top.
14. Run `./runflask.bat`
15. Navigate to the webpage in your browser (http://127.0.0.1:5000)
16. Enjoy!
