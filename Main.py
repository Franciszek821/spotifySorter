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

playlists = ["older", "1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]
playlist_id = None



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

def get_playlist_id_by_name(sp, playlist_name):
    limit = 50
    offset = 0

    while True:
        playlists = sp.current_user_playlists(limit=limit, offset=offset)
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                return playlist['id']
        if playlists['next']:
            offset += limit
        else:
            break

    return None  # Not found



for pla in playlists:
    pl_id = get_playlist_id_by_name(sp, pla)
    if pl_id:
        sp.current_user_unfollow_playlist(pl_id)



def checkIfPlaylistExists(playlist_name):
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
        if pl['name'] == playlist_name:
            playlist_id=pl['id']
            return True
    return False


for pla in playlists:
    if checkIfPlaylistExists(str(pla)) == False:
        sp.user_playlist_create(user=user_id, name=pla, public=False)


def checkIfSongInPlaylist(song_id, pl_id):
    songs = []
    limit = 50
    offset = 0

    while True:
        response = sp.playlist_tracks(playlist_id=pl_id, limit=limit, offset=offset)
        songs.extend(response['items'])
        if response['next']:
            offset += limit
        else:
            break


    for pl in songs:
        if pl['track']['id'] == song_id:
            return True
    return False



for i in liked_tracks[:10]:
    song_id = i['track']['id']
    track = sp.track(song_id)
    year = int(track['album']['release_date'].split("-")[0])

    for pla in playlists:
        if pla == "older":
            continue

        playlist_id = get_playlist_id_by_name(sp, str(pla))
        if year >= int(pla) and year < int(pla) + 10:
            if not checkIfSongInPlaylist(song_id, playlist_id):
                sp.playlist_add_items(playlist_id=playlist_id, items=[song_id])
            continue

    if year < 1950:
        playlist_id = get_playlist_id_by_name(sp, "older")
        if not checkIfSongInPlaylist(song_id, playlist_id):
            sp.playlist_add_items(playlist_id=playlist_id, items=[song_id])
        continue














