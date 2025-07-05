import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import time
from spotipy.exceptions import SpotifyException
import random

playlistsLIST = ["2020", "2010", "2000", "1990", "1980", "1970", "1960", "1950", "1940", "older"]

def safe_spotify_call(func, *args, max_retries=5, **kwargs):
    wait_time = 1
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 1))
                max_wait = 120  # cap max wait at 2 minutes
                wait = min(retry_after, max_wait)
                print(f"[Rate limited] Waiting {wait}s before retry (Attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
            else:
                print(f"[SpotifyException] Attempt {attempt+1}/{max_retries}: {e}")
                backoff = wait_time + random.uniform(0, 1)
                time.sleep(backoff)
                wait_time *= 2
        except Exception as e:
            print(f"[Exception] Attempt {attempt+1}/{max_retries}: {e}")
            backoff = wait_time + random.uniform(0, 1)
            time.sleep(backoff)
            wait_time *= 2
    raise Exception(f"Max retries exceeded for Spotify API call: {func.__name__}")

def get_all_liked_tracks(sp, total_to_get):
    all_tracks = []
    offset = 0
    limit = 50

    while len(all_tracks) < total_to_get:
        remaining = total_to_get - len(all_tracks)
        current_limit = min(limit, remaining)
        results = safe_spotify_call(sp.current_user_saved_tracks, limit=current_limit, offset=offset)
        items = results.get('items', [])
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
        items = response.get('items', [])
        if not items:
            break
        track_names.extend(items)
        if not response.get('next'):
            break
        offset += limit

    return track_names

def get_all_playlists(sp):
    playlists = ["liked"]
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        items = response.get('items', [])
        for item in items:
            playlists.append(item.get('name'))
        if not response.get('next'):
            break
        offset += limit

    return playlists

def get_playlist_id_by_name(sp, playlist_name):
    limit = 50
    offset = 0

    while True:
        playlists = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        for pla in playlists.get('items', []):
            if pla.get('name', '').lower() == playlist_name.lower():
                return pla.get('id')
        if not playlists.get('next'):
            break
        offset += limit

    return None

def get_artist_id(sp, artist_name):
    result = safe_spotify_call(sp.search, q=f'artist:{artist_name}', type='artist', limit=1)
    artists = result.get('artists', {}).get('items', [])
    if artists:
        return artists[0].get('id')
    return None

def checkIfPlaylistExists(sp, playlist_name):
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        items = response.get('items', [])
        for pl in items:
            if pl.get('name') == playlist_name:
                return True
        if not response.get('next'):
            break
        offset += limit

    return False

def checkIfSongInPlaylist(sp, song_id, playlist_id):
    limit = 50
    offset = 0

    while True:
        response = safe_spotify_call(sp.playlist_tracks, playlist_id=playlist_id, limit=limit, offset=offset)
        items = response.get('items', [])
        for pl in items:
            track = pl.get('track')
            if track and track.get('id') == song_id:
                return True
        if not response.get('next'):
            break
        offset += limit

    return False

def sort(sp, total_to_get, playlist):
    if playlist == "liked":
        tracks = get_all_liked_tracks(sp, total_to_get)
    else:
        source_playlist_id = get_playlist_id_by_name(sp, playlist)
        if not source_playlist_id:
            print(f"Playlist '{playlist}' not found.")
            return
        tracks = get_all_track_names(sp, source_playlist_id, total_to_get)

    if not tracks:
        print("No tracks found for sorting.")
        return

    existing_playlists = get_all_playlists(sp)
    user_id = safe_spotify_call(sp.current_user).get('id')

    for i in tracks[:total_to_get]:
        time.sleep(0.2)
        song_id = i.get('track', {}).get('id')
        if not song_id:
            continue

        track = safe_spotify_call(sp.track, song_id)
        release_date = track.get('album', {}).get('release_date', '1900-01-01')
        try:
            year = int(release_date.split("-")[0])
        except ValueError:
            year = 1900

        added_to_playlist = False

        for pla in playlistsLIST:
            if pla == "older":
                continue
            start_year = int(pla)
            if start_year <= year < start_year + 10:
                playlist_name = f"{pla} from {playlist}"
                if playlist_name not in existing_playlists:
                    safe_spotify_call(
                        sp.user_playlist_create,
                        user=user_id,
                        name=playlist_name,
                        public=False,
                        description="Made by Spotify Sorter"
                    )
                    existing_playlists = get_all_playlists(sp)

                target_playlist_id = get_playlist_id_by_name(sp, playlist_name)
                if target_playlist_id and not checkIfSongInPlaylist(sp, song_id, target_playlist_id):
                    safe_spotify_call(sp.playlist_add_items, playlist_id=target_playlist_id, items=[f"spotify:track:{song_id}"])
                added_to_playlist = True
                break

        if not added_to_playlist and year < 1940:
            if "older" not in existing_playlists:
                safe_spotify_call(
                    sp.user_playlist_create,
                    user=user_id,
                    name="older",
                    public=False,
                    description="Made by Spotify Sorter"
                )
                existing_playlists = get_all_playlists(sp)

            older_playlist_id = get_playlist_id_by_name(sp, "older")
            if older_playlist_id and not checkIfSongInPlaylist(sp, song_id, older_playlist_id):
                safe_spotify_call(sp.playlist_add_items, playlist_id=older_playlist_id, items=[f"spotify:track:{song_id}"])

def clear_playlists(sp):
    limit = 50
    offset = 0
    while True:
        playlists_response = safe_spotify_call(sp.current_user_playlists, limit=limit, offset=offset)
        playlists = playlists_response.get('items', [])

        for pla in playlists:
            if pla.get('description') == "Made by Spotify Sorter":
                safe_spotify_call(sp.current_user_unfollow_playlist, pla['id'])

        if not playlists_response.get('next'):
            break
        offset += limit

def top20_songs(sp, selected_time):
    playlist_name = f"Top20 {selected_time}"    
    topSongs = safe_spotify_call(sp.current_user_top_tracks, limit=20, offset=0, time_range=selected_time)

    if not checkIfPlaylistExists(sp, playlist_name):
        user_id = safe_spotify_call(sp.current_user).get('id')
        safe_spotify_call(
            sp.user_playlist_create,
            user=user_id,
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )

    playlist_id = get_playlist_id_by_name(sp, playlist_name)
    if playlist_id:
        for song in topSongs.get('items', []):
            if not checkIfSongInPlaylist(sp, song['id'], playlist_id):
                safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])

def artistTop(sp, selected_artist):
    artist_id = get_artist_id(sp, selected_artist)
    if artist_id is None:
        return f"Artist '{selected_artist}' not found."

    topSongs = safe_spotify_call(sp.artist_top_tracks, artist_id)
    if not topSongs.get('tracks'):
        return f"No top tracks found for artist '{selected_artist}'."

    playlist_name = f"Top10 {selected_artist}"
    if not checkIfPlaylistExists(sp, playlist_name):
        safe_spotify_call(
            sp.user_playlist_create,
            user=safe_spotify_call(sp.current_user).get('id'),
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
    playlist_name = f"topArtistsSongs {selected_time}"
    if not checkIfPlaylistExists(sp, playlist_name):
        safe_spotify_call(
            sp.user_playlist_create,
            user=safe_spotify_call(sp.current_user).get('id'),
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )
    playlist_id = get_playlist_id_by_name(sp, playlist_name)

    for art in artist.get('items', []):
        topSongs = safe_spotify_call(sp.artist_top_tracks, art['id'])
        if not topSongs.get('tracks'):
            continue

        for song in topSongs['tracks']:
            if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
                safe_spotify_call(sp.playlist_add_items, playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])

def getName(sp):
    try:
        user_info = sp.current_user()
        display_name = user_info.get('display_name')
        return display_name
    except Exception as e:
        print(f"Error fetching user name: {e}")
        return None
