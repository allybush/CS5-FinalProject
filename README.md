# CS5-FinalProject Instructions

## Set Up

1. Install Python 3.8-64 version or use any 3.8-3.9 version you already have installed. (https://www.python.org/downloads/release/python-380/)
2. Use an IDE of your choice (we used PyCharm) to open "model folder"
3. Configure the interpreter for Python 3.8 (the version you just installed) and install the necessary packages (keras, tensorflow, numpy, PIL, matplotlib, librosa, pydub, spotipy, ffmpeg, ffprobe). 
4. Download the dataset from this link https://drive.google.com/drive/folders/16-_cpPry8Q52JSqxmEAhOwCARg-pBR8k?usp=sharing (if this was successful, skip steps 6-10).

——————skip if 4 was successful ———————

6. Create a folder anywhere on your computer titled "Data" with 7 subfolders titled "pop", "rock", "classical", "jazz", "metal", "country", and "rap"
7. Navigate to `dataset.py` and follow the instructions at the top.
8. Run `dataset.py`
10. At this point, you might encounter a WINERROR. To solve this, download ffmpeg from this link (https://ffmpeg.org/download.html) and ensure that the three files in the ffmpeg package (fmpeg.exe, ffprobe.exe, ffplay.exe) are located on your path so they can be run.

——————————————————————————————————————


12. After procuring the dataset, navigate to `trainmodel.py`. (You should have a massive folder and 7 smaller folders of roughly 800 RGB images each).
13. Follow the instructions at the top of `trainmodel.py`
14. Run `trainmodel.py`
15. Navigate to webpage_stuff/spotify_webpage and locate `runmodel.py`
16. Follow the instructions at the top.
17. Run `./runflask.bat` to host the server.
18. Navigate to the webpage in your browser (http://127.0.0.1:5000)
19. Enjoy!
