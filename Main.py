import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

app = Flask(__name__)


# Load local .env file variables if running locally
#load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public playlist-modify-private user-library-read"
))

user_id = sp.current_user()['id']

playlists = ["older", "1940", "1950", "1960", "1970", "1980", "1990", "2000", "2010", "2020"]
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


def button():
    for i in liked_tracks[:100]:
        song_id = i['track']['id']
        track = sp.track(song_id)
        year = int(track['album']['release_date'].split("-")[0])

        for pla in playlists:
            if pla == "older":
                continue

            if year >= int(pla) and year < int(pla) + 10:
                if not checkIfPlaylistExists(str(pla)):
                    sp.user_playlist_create(user=user_id, name=pla, public=False)

                playlist_id = get_playlist_id_by_name(sp, str(pla))

                if playlist_id and not checkIfSongInPlaylist(song_id, playlist_id):
                    sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])
                break 

        if year < 1940:
            if not checkIfPlaylistExists("older"):
                sp.user_playlist_create(user=user_id, name="older", public=False)

            playlist_id = get_playlist_id_by_name(sp, "older")

            if playlist_id and not checkIfSongInPlaylist(song_id, playlist_id):
                sp.playlist_add_items(playlist_id=playlist_id, items=[f"spotify:track:{song_id}"])



@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        try:
            button()
            message = "Playlists created and songs added successfully!"
        except Exception as e:
            message = f"An error occurred: {str(e)}"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)










