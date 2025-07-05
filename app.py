from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from Main import sort, clear_playlists, top20_songs, artistTop, topArtistsSongs, get_all_playlists, getName
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

def get_token():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative user-top-read"
    )

    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception("No token info in session")

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session["token_info"] = token_info

    return token_info['access_token']

def get_spotify_client():
    access_token = get_token()
    return spotipy.Spotify(auth=access_token, requests_timeout=30)

@app.route("/")
def main():
    is_logged_in = "token_info" in session
    return render_template("Main/index.html", is_logged_in=is_logged_in)

@app.route('/about')
def about_page():
    is_logged_in = "token_info" in session
    name = None
    if is_logged_in:
        sp = get_spotify_client()
        name = getName(sp)
    return render_template('About/index.html', is_logged_in=is_logged_in, name=name)

@app.route('/help')
def help_page():
    is_logged_in = "token_info" in session
    name = None
    if is_logged_in:
        sp = get_spotify_client()
        name = getName(sp)
    return render_template("Help/index.html", is_logged_in=is_logged_in, name=name)

@app.route("/functions", methods=["GET", "POST"])
def functions():
    is_logged_in = "token_info" in session
    if not is_logged_in:
        return redirect(url_for('login'))

    sp = get_spotify_client()
    name = getName(sp)
    playlists = get_all_playlists(sp)
    message = None

    if request.method == "POST":
        action = request.form.get('action')
        if action == 'sort':
            selected_Songs = request.form.get('numSort')
            selected_playlist = request.form.get("selected_option")
            sort(sp, int(selected_Songs), selected_playlist)
            message = "Your liked songs have been sorted and added to the playlists."
        elif action == 'clear':
            clear_playlists(sp)
            message = "All playlists have been cleared."
        elif action == 'top20_songs':
            selected_time = request.form.get('time')
            if selected_time is not None:
                top20_songs(sp, selected_time)
                message = "Top 20 songs playlist has been created."
            else:
                message = "Choose time"
        elif action == 'top10_artist':
            selected_artist = request.form.get('artist')
            if selected_artist is not None:
                message = artistTop(sp, selected_artist)
            else:
                message = "Choose artist"
        elif action == 'topArtistsSongs':
            selected_timeArt = request.form.get('timeTopArtist')
            if selected_timeArt is not None:
                topArtistsSongs(sp, selected_timeArt)
                message = "Playlist have been created"
            else:
                message = "Choose time"

        playlists = get_all_playlists(sp)

    return render_template("Functions/index.html", message=message, my_list=playlists, is_logged_in=is_logged_in, name=name)

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative user-top-read"
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data (token, etc.)
    return redirect(url_for('main'))

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative user-top-read"
    )

    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('main'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
