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

def get_user_playlists(limit=20, offset=0):
    playlists = sp.current_user_playlists(limit=limit, offset=offset)
    for pl in playlists['items']:
        print(f"Playlist: {pl['name']}")
get_user_playlists()

playlist = sp.user_playlist_create(user=user_id, name="Playlist", public=False, collaborative=False, description='Playlist created by Spotipy')






