import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os





playlistsLIST = ["2020", "2010", "2000", "1990", "1980", "1970", "1960", "1950", "1940", "older"]

def get_all_liked_tracks(sp, total_to_get):
    all_tracks = []
    offset = 0
    limit = 50

    while len(all_tracks) < total_to_get:
        remaining = total_to_get - len(all_tracks)
        current_limit = min(limit, remaining)

        results = sp.current_user_saved_tracks(limit=current_limit, offset=offset)
        items = results['items']

        if not items:
            break

        all_tracks.extend(items)
        offset += current_limit

    return all_tracks



def get_playlist_id_by_name(sp, playlist_name):
    limit = 50
    offset = 0

    while True:
        playlists = sp.current_user_playlists(limit=limit, offset=offset)
        for pla in playlists['items']:
            if pla['name'].lower() == playlist_name.lower():
                return pla['id']
        if playlists['next']:
            offset += limit
        else:
            break

    return None  # Not found


def get_artist_id(sp, artist_name):
    result = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if result['artists']['items']:
        return result['artists']['items'][0]['id']
    return None




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


def sort(sp, user_id, total_to_get):

    
    playlist_id = None
    # Fetch all liked songs
    liked_tracks = get_all_liked_tracks(sp, total_to_get)
    print([p['name'] for p in sp.current_user_playlists(limit=50)['items']])

    for i in liked_tracks[:total_to_get]: # Limit to first 1 tracks for testing
        song_id = i['track']['id']
        track = sp.track(song_id)
        year = int(track['album']['release_date'].split("-")[0])

        for pla in playlistsLIST:
            if pla == "older":
                continue

            if year >= int(pla) and year < int(pla) + 10:
                print(f"Playlist ID for {pla}: {playlist_id}")
                if not playlist_id:
                    sp.user_playlist_create(
                        user=user_id,
                        name=pla,
                        public=False,
                        description="Made by Spotify Sorter"
                    )

                    

                playlist_id = get_playlist_id_by_name(sp, pla)
                if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                    sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])
                    #print(f"chuj")

                break 

        if year < 1940:
            if not checkIfPlaylistExists(sp, "older"):
                sp.user_playlist_create(user=user_id, name="older", public=False)

            playlist_id = get_playlist_id_by_name(sp, "older")

            if playlist_id and not checkIfSongInPlaylist(sp, song_id, playlist_id):
                sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])

def clear_playlists(sp):
    limit = 50
    offset = 0
    while True:
        playlists_response = sp.current_user_playlists(limit=limit, offset=offset)
        playlists = playlists_response['items']
        
        for pla in playlists:
            if pla.get('description') == "Made by Spotify Sorter":
                sp.current_user_unfollow_playlist(pla['id'])
        
        if playlists_response.get('next'):
            offset += limit
        else:
            break


def top20_songs(sp, selected_time):
    topSongs = sp.current_user_top_tracks(limit=20, offset=0, time_range=selected_time)
    for song in topSongs['items']:
        #print("Adding song to Top20 playlist:", song['name'])
        if not checkIfPlaylistExists(sp, "Top20" + str(selected_time)):
            sp.user_playlist_create(
                user=sp.current_user()['id'],
                name=f"Top20{selected_time}",
                public=False,
                description="Made by Spotify Sorter"
            )

        playlist_id = get_playlist_id_by_name(sp, "Top20" + str(selected_time))
        if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
            sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])

def artistTop(sp, selected_artist):
    artist_id = get_artist_id(sp, selected_artist)
    if artist_id is None:
        return f"Artist '{selected_artist}' not found."
    
    topSongs = sp.artist_top_tracks(artist_id)
    
    if 'tracks' not in topSongs or not topSongs['tracks']:
        return f"No top tracks found for artist '{selected_artist}'."
    
    playlist_name = f"Top10 {selected_artist}"
    if not checkIfPlaylistExists(sp, playlist_name):
        sp.user_playlist_create(
            user=sp.current_user()['id'],
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )

    playlist_id = get_playlist_id_by_name(sp, playlist_name)

    for song in topSongs['tracks']:
        if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
            sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])
    
    return f"Top 10 songs playlist for '{selected_artist}' has been created."


#categories = ["Made For You", "New Releases", "Summer", "Hip-Hop", "Pop", "Mood", "Charts", "Indie", "Trending", "Dance/Electronic", "Rock", "Discover", "Chill", "Party", "Disco Polo", "RADAR", "Workout", "EQUAL", "Decades", "GLOW", "K-pop", "Sleep", "At Home", "Latin", "Love", "Fresh Finds", "Metal", "Anime", "Jazz", "Classical", "Netflix", "Focus", "Folk & Acoustic", "Soul", "Kids & Family", "Gaming", "TV & Movies", "R&B", "Instrumental"]

def testing(sp, user_id):

    artist = sp.current_user_top_artists(limit=5, offset=0, time_range='medium_term')
    playlist_name = f"topArtistsSongs"
    if not checkIfPlaylistExists(sp, playlist_name):
        sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False,
            description="Made by Spotify Sorter"
        )
    playlist_id = get_playlist_id_by_name(sp, playlist_name)
    
    for art in artist['items']:
        topSongs = sp.artist_top_tracks(art['id'])
        if 'tracks' not in topSongs or not topSongs['tracks']:
            continue

        for song in topSongs['tracks']:
            if playlist_id and not checkIfSongInPlaylist(sp, song['id'], playlist_id):
                sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song['id']}"])


            
    










#TODO:
# make a loading wheel when sorting

#current_user_top_artists(limit=20, offset=0, time_range='medium_term') this and top 10 from 5 artists

# 2. Add a button to sort liked songs by genre
# 3. Add a button that makes a daily playlist with liked songs sorted by genre (25 songs)
# 4. Add a button 


#artist_related_artists(artist_id)
#artist_top_tracks(artist_id)
#current_user_top_tracks(limit=20, offset=0, time_range='medium_term')
#recommendation_genre_seeds()
#user(user)