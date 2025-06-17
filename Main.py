import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your actual Spotify app credentials
CLIENT_ID = 'ba66ea8afc314359ba4a3af2e8edfbf8'
CLIENT_SECRET = '4293e5a50eae4fe18f82b28309763210'
REDIRECT_URI = 'http://localhost:5000'

# Set up the Spotipy client with proper scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read"
))

# Fetch liked (saved) tracks
results = sp.current_user_saved_tracks(limit=1)

print("Your first 1 liked songs:")
for idx, item in enumerate(results['items'], 1):
    track = item['track']
    print(f"{idx}. {track['name']} - {track['artists'][0]['name']}")
