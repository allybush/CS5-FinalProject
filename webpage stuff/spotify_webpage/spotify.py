import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8bded2f340e44e03a981384c95b90841",
                                                           client_secret="9d78bf687193476bb8bc81707f439431"))


def search(name):
    try:
        if(name != ''):
            print("1")
            results = sp.search(name, limit=20, market='US')
            # print(results)
            tracks = results['tracks']['items']
            print("2")
            # for track in tracks:
            #     print("3")
            #     if(track['preview_url'] == None):
            #         print('issue with a track!')
            #         print(track['uri'])
            #         track_data = sp.tracks([track['uri']], market='US')
            #         print('get track data!')
            #         print(track_data)

            return tracks
    except Exception as err:
        print(err)
    return "NOTFOUND"


def getTrack(id):
    if(id != ''):
        results = sp.track(track_id=id)
    return []

# getTrack('1ZM8toCOlnfBKJdvR8GqUq?si=3d4c58e98973402b')

def getSongWAV():
    # sp.track()
    print('test')
