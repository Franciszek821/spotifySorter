import spotipy
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ba66ea8afc314359ba4a3af2e8edfbf8",
    client_secret="4293e5a50eae4fe18f82b28309763210",
    redirect_uri="http://localhost:5000",
    scope="playlist-modify-public playlist-modify-private user-library-read"
))

user_id = sp.current_user()['id']

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

# Print first few
for idx, item in enumerate(liked_tracks[:1], 1):
    track = item['track']
    print(f"{idx}. {track['name']} – {track['artists'][0]['name']}")
    uris = [item['track']['uri']]

print(f"\nTotal liked tracks found: {len(liked_tracks)}")

playlist = sp.user_playlist_create(user=user_id, name="CHUJKURWA", public=False)
print("Nowa playlista ID:", playlist['id'])

sp.playlist_add_items(playlist_id=playlist['id'], items=uris)
print("Dodano utwory do playlisty.")


