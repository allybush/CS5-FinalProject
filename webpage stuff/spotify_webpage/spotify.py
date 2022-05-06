import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8bded2f340e44e03a981384c95b90841",
                                                           client_secret="9d78bf687193476bb8bc81707f439431"))



def search(name):
    if(name != ''):
        results = sp.search(q=name, limit=5, market='US')
        return results['tracks']['items']
    return []


def getTrack(id):
    if(id != ''):
        results = sp.track(track_id=id)
    return []


getTrack('1ZM8toCOlnfBKJdvR8GqUq?si=3d4c58e98973402b')

def getSongWAV():
    # sp.track()
    print('test')
