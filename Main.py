import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os






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



#for pla in playlists:
#    pl_id = get_playlist_id_by_name(sp, pla)
#    if pl_id:
#        sp.current_user_unfollow_playlist(pl_id)



def checkIfPlaylistExists(sp, playlist_name):
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


def checkIfSongInPlaylist(sp, song_id, pl_id):
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


def sort(sp, user_id):

    playlists = ["2020", "2010", "2000", "1990", "1980", "1970", "1960", "1950", "1940", "older"]
    playlist_id = None
    # Fetch all liked songs
    liked_tracks = get_all_liked_tracks(sp)

    playlist_cache = {}  # {year_str: playlist_id}

    for i in liked_tracks[:3]:
        song_id = i['track']['id']
        track = sp.track(song_id)
        year = int(track['album']['release_date'].split("-")[0])

        # Determine target playlist name
        target_playlist = "older" if year < 1940 else None
        for pla in playlists[:2]:
            if pla != "older" and int(pla) <= year < int(pla) + 10:
                target_playlist = pla
                break

        if not target_playlist:
            continue  # Skip unknown years

        # Create playlist if needed and cache it
        if target_playlist not in playlist_cache:
            if not checkIfPlaylistExists(sp, target_playlist):
                sp.user_playlist_create(user=user_id, name=target_playlist, public=False)
            playlist_id = get_playlist_id_by_name(sp, target_playlist)
            playlist_cache[target_playlist] = playlist_id
        else:
            playlist_id = playlist_cache[target_playlist]

        # Only add song if not already in playlist
        if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
            sp.playlist_add_items(playlist_id=playlist_id, items=song_id)














