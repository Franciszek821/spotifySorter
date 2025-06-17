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


def checkIfPlaylistExists(playlist_name_to_find):
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

    print("All your playlists:")
    for pl in playlists:
        print(f"- {pl['name']}")

    # Check if playlist exists
    for pl in playlists:
        if pl['name'] == playlist_name_to_find:
            print(f"Playlist '{playlist_name_to_find}' FOUND.")
            return True

    print(f"Playlist '{playlist_name_to_find}' NOT found.")
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

if checkIfPlaylistExists("Moja playlista #7") == False:
    plajlista = sp.user_playlist_create(user=user_id, name="Moja playlista #7", public=False)

'''
# Print first few
for idx, item in enumerate(liked_tracks[:3], 1):
    track = item['track']
    uris = [item['track']['uri']]
    print (int(track['album']['release_date'].split("-")[0]))
    if int(track['album']['release_date'].split("-")[0]) >= 2000:
        if not is_track_in_playlist(sp, plajlista['id'], uris):
            sp.playlist_add_items(playlist_id=plajlista['id'], items=uris)
        
'''






