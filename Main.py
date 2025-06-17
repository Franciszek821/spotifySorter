import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private user-library-read"
))


user_id = sp.current_user()['id']

playlist_id=None

'''
def get_all_liked_tracks(sp):
    all_tracks = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results['items']
        if not items:
            break
        all_tracks.extend(items)
        offset += limit

    return all_tracks

# Fetch all liked songs
liked_tracks = get_all_liked_tracks(sp)
'''


def checkIfPlaylistExists(playlist_id):
    playlists = []
    limit = 50
    offset = 0

    while True:
        response = sp.current_user_playlists(limit=limit, offset=offset)
        playlists.extend(response['items'])
        if response['next']:
            offset += limit
        else:
            break


    for pl in playlists:
        print(pl['id'])
        if pl['id'] == playlist_id:
            return True
    return False


'''
def is_track_in_playlist(sp, playlist_id, track_uri):
    limit = 100
    offset = 0

    while True:
        response = sp.playlist_items(playlist_id, limit=limit, offset=offset)
        items = response['items']
        # Check each track in the current batch
        for item in items:
            if item['track']['uri'] == track_uri:
                return True
        if response['next']:
            offset += limit
        else:
            break
    return False

'''

#if checkIfPlaylistExists("playlist_2000") == False:
    #playlist_2000 = sp.user_playlist_create(user=user_id, name="playlist_2000", public=False)
    #playlist_id=playlist_2000['id']


playlist_2000 = sp.user_playlist_create(user=user_id, name="Franciszek", public=False)
# Fetch all playlists
def get_all_playlists(sp):
    all_playlists = []
    offset = 0
    limit = 50

    while True:
        results = sp.current_user_playlists(limit=limit, offset=offset)
        items = results['items']
        if not items:
            break
        all_playlists.extend([item['name'] for item in items])
        offset += limit

    return all_playlists

print("Fetching all playlists...")
print(get_all_playlists(sp))


playlists = []
limit = 50
offset = 0

#while True:
        #response = sp.current_user_playlists(limit=limit, offset=offset)
        #playlists.extend(response['items'])
        #if response['next']:
        #    offset += limit
        #else:
        #    break




'''
# Print first few
for idx, item in enumerate(liked_tracks[:3], 1):
    track = item['track']
    uris = [item['track']['uri']]
    print (int(track['album']['release_date'].split("-")[0]))
    if int(track['album']['release_date'].split("-")[0]) >= 2000:
        if not is_track_in_playlist(sp, playlist_2000['id'], uris):
            sp.playlist_add_items(playlist_id=playlist_2000['id'], items=uris)
        
'''






