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

    for i in liked_tracks[:10]: # Limit to first 10 tracks for testing
        song_id = i['track']['id']
        track = sp.track(song_id)
        year = int(track['album']['release_date'].split("-")[0])

        for pla in playlists:
            if pla == "older":
                continue

            if year >= int(pla) and year < int(pla) + 10:
                playlist_id = get_playlist_id_by_name(sp, pla)
                if not playlist_id:
                    sp.user_playlist_create(user=user_id, name=pla, public=False)
                    print(f"Created playlist {pla}")
                    playlist_id = get_playlist_id_by_name(sp, pla)


                if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                    sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])
                    print(f"Added {track['name']} to playlist {pla}")
                break 

        if year < 1940:
            if not checkIfPlaylistExists(sp, "older"):
                sp.user_playlist_create(user=user_id, name="older", public=False)

            playlist_id = get_playlist_id_by_name(sp, "older")

            if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])














