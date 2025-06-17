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



def checkIfPlaylistExists(playlist_name_to_find):
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
        if pl['name'] == playlist_name_to_find:
            return True
        
    return False


if not checkIfPlaylistExists("playlist2000"):
    playlist2000 = sp.user_playlist_create(user=user_id, name="playlist2000", public=False)


# Print first few
for idx, item in enumerate(liked_tracks[:3], 1):
    track = item['track']
    uris = [item['track']['uri']]
    print (int(track['album']['release_date'].split("-")[0]))
    if int(track['album']['release_date'].split("-")[0]) >= 2000:
        sp.playlist_add_items(playlist_id=playlist2000['id'], items=uris)
        





#print(f"\nTotal liked tracks found: {len(liked_tracks)}")


#playlist = sp.user_playlist_create(user=user_id, name="CHUJKURWA", public=False)
#print("Nowa playlista ID:", playlist['id'])
#
#sp.playlist_add_items(playlist_id=playlist['id'], items=uris)
#print("Dodano utwory do playlisty.")


