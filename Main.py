import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
from spotipy.exceptions import SpotifyException

# Define decades
playlistsLIST = ["2020", "2010", "2000", "1990", "1980", "1970", "1960", "1950", "1940", "older"]

# Retry-safe Spotify API call wrapper
def safe_spotify_call(func, *args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                wait_time = int(e.headers.get("Retry-After", 1))
                print(f"[Rate limited] Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"[Retry {attempt+1}/{max_retries}] Error: {e}")
            time.sleep(2)
    raise Exception("Max retries exceeded for Spotify API call")

def get_all_liked_tracks(sp, total_to_get):
    all_tracks = []
    offset = 0
    limit = 50

    while len(all_tracks) < total_to_get:
        remaining = total_to_get - len(all_tracks)
        current_limit = min(limit, remaining)

        results = safe_spotify_call(sp.current_user_saved_tracks, limit=current_limit, offset=offset)
        items = results['items']

        if not items:
            break

        all_tracks.extend(items)
        offset += current_limit

    return all_tracks

def get_all_track_names(sp, playlist_id, total_to_get):
    track_names = []
    limit = 50
    offset = 0

    while len(track_names) < total_to_get:
        response = safe_spotify_call(sp.playlist_tracks, playlist_id=playlist_id, limit=limit, offset=offset)
        for item in response['items']:
            track = item
            if track:
                track_names.append(track)

        if response['next']:
            offset += limit
        else:
            break

    return track_names

def get_all_playlists(sp):
    playlists = ["liked"]
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        for item in response['items']:
            playlists.append(item['name'])
        if response['next']:
            offset += limit
        else:
            break

    return playlists

def get_playlist_id_by_name(sp, playlist_name):
    limit = 50
    offset = 0

    while True:
        playlists = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        for pla in playlists['items']:
            if pla['name'].lower() == playlist_name.lower():
                return pla['id']
        if playlists['next']:
            offset += limit
        else:
            break

    return None

def get_artist_id(sp, artist_name):
    result = safe_spotify_call(sp.search, q=f'artist:{artist_name}', type='artist', limit=1)
    if result['artists']['items']:
        return result['artists']['items'][0]['id']
    return None

def checkIfPlaylistExists(sp, playlist_name):
    playlists = []
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        playlists.extend(response['items'])
        if response['next']:
            offset += limit
        else:
            break

    for pl in playlists:
        if pl['name'] == playlist_name:
            return True
    return False

def checkIfSongInPlaylist(sp, song_id, playlist_id):
    songs = []
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.playlist_tracks, playlist_id=playlist_id, limit=limit, offset=offset)
        songs.extend(response['items'])
        if response['next']:
            offset += limit
        else:
            break

    for pl in songs:
        if pl['track']['id'] == song_id:
            return True
    return False

def sort(sp, total_to_get, playlist):
    playlist_id = None
    if playlist == "liked":
        tracks = get_all_liked_tracks(sp, total_to_get)
    else:
        playlist_id = get_playlist_id_by_name(sp, playlist)
        tracks = get_all_track_names(sp, playlist_id, total_to_get)

    for i in tracks[:total_to_get]:
        time.sleep(0.2)
        song_id = i['track']['id']
        track = safe_spotify_call(sp.track, song_id)
        year = int(track['album']['release_date'].split("-")[0])

        for pla in playlistsLIST:
            if pla == "older":
                continue

            if year >= int(pla) and year < int(pla) + 10:
                playlists = get_all_playlists(sp)
                if pla not in playlists:
                    safe_spotify_call(
                        sp.user_playlist_create,
                        user=safe_spotify_call(sp.current_user)['id'],
                        name=f"{pla} from {playlist}",
                        public=False,
                        description="Made by Spotify Sorter"
                    )

                playlist_id = get_playlist_id_by_name(sp, pla)
                if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                    safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])
                break

        if year < 1940:
            if not checkIfPlaylistExists(sp, "older"):
                safe_spotify_call(
                    sp.user_playlist_create,
                    user=safe_spotify_call(sp.current_user)['id'],
                    name="older",
                    public=False,
                    description="Made by Spotify Sorter"
                )

            playlist_id = get_playlist_id_by_name(sp, "older")
            if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])

def clear_playlists(sp):
    limit = 50
    offset = 0
    while True:
        playlists_response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        playlists = playlists_response['items']
        
        for pla in playlists:
            if pla.get('description') == "Made by Spotify Sorter":
                safe_spotify_call(sp.current_user_unfollow_playlist, pla['id'])
        
        if playlists_response.get('next'):
            offset += limit
        else:
            break

def top20_songs(sp, selected_time):
    topSongs = safe_spotify_call(sp.current_user_top_tracks, limit=20, offset=0, time_range=selected_time)
    for song in topSongs['items']:
        if not checkIfPlaylistExists(sp, "Top20" + str(selected_time)):
            safe_spotify_call(
                sp.user_playlist_create,
                user=safe_spotify_call(sp.current_user)['id'],
                name=f"Top20{selected_time}",
                public=False,
                description="Made by Spotify Sorter"
            )

        playlist_id = get_playlist_id_by_name(sp, "Top20" + str(selected_time))
        if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
            safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])

def artistTop(sp, selected_artist):
    artist_id = get_artist_id(sp, selected_artist)
    if artist_id is None:
        return f"Artist '{selected_artist}' not found."
    
    topSongs = safe_spotify_call(sp.artist_top_tracks, artist_id)
    if 'tracks' not in topSongs or not topSongs['tracks']:
        return f"No top tracks found for artist '{selected_artist}'."
    
    playlist_name = f"Top10 {selected_artist}"
    if not checkIfPlaylistExists(sp, playlist_name):
        safe_spotify_call(
            sp.user_playlist_create,
            user=safe_spotify_call(sp.current_user)['id'],
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )

    playlist_id = get_playlist_id_by_name(sp, playlist_name)

    for song in topSongs['tracks']:
        if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
            safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])
    
    return f"Top 10 songs playlist for '{selected_artist}' has been created."

def topArtistsSongs(sp, selected_time):
    artist = safe_spotify_call(sp.current_user_top_artists, limit=5, offset=0, time_range=selected_time)
    playlist_name = f"topArtistsSongs"
    if not checkIfPlaylistExists(sp, playlist_name):
        safe_spotify_call(
            sp.user_playlist_create,
            user=safe_spotify_call(sp.current_user)['id'],
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )
    playlist_id = get_playlist_id_by_name(sp, playlist_name)
    
    for art in artist['items']:
        topSongs = safe_spotify_call(sp.artist_top_tracks, art['id'])
        if 'tracks' not in topSongs or not topSongs['tracks']:
            continue

        for song in topSongs['tracks']:
            if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
                safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])

def getName(sp):
    user_info = sp.current_user()
    username = user_info['id']
    return username


# make the timeout higher
# Top 10 songs from your top 5 artists  make it possible to choose the time range
# make it pretty
# test everything few times
# make a test design




