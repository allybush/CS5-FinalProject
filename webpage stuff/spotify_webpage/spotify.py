import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8bded2f340e44e03a981384c95b90841",
                                                           client_secret="9d78bf687193476bb8bc81707f439431"))

#searches spotify for that song, returns top 20 if more than 20.
def search(name):
    try:
        if(name != ''):
            #uses spotipy, a library for python and spotify API
            results = sp.search(name, limit=20, market='US')
            #sifts through json for the songs.
            tracks = results['tracks']['items']
            return tracks
    except Exception as err:
        print(err)
    return "NOTFOUND"
