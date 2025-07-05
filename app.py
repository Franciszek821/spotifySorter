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

def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative user-top-read"
    )

def get_token():
    sp_oauth = get_spotify_oauth()
    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception("No token info in session")
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session["token_info"] = token_info
    return token_info

@app.route("/")
def main():
    is_logged_in = "token_info" in session
    return render_template("Main/index.html", is_logged_in=is_logged_in)

@app.route('/about')
def about_page():
    is_logged_in = "token_info" in session
    name = None
    if is_logged_in:
        try:
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            name = getName(sp)
        except Exception as e:
            print(f"Error in about_page: {e}")
    return render_template('About/index.html', is_logged_in=is_logged_in, name=name)

@app.route('/help')
def help_page():
    is_logged_in = "token_info" in session
    name = None
    if is_logged_in:
        try:
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            name = getName(sp)
        except Exception as e:
            print(f"Error in help_page: {e}")
    return render_template("Help/index.html", is_logged_in=is_logged_in, name=name)

@app.route("/functions", methods=["GET", "POST"])
def functions():
    is_logged_in = "token_info" in session
    if not is_logged_in:
        return redirect("/")

    name = None
    try:
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
        name = getName(sp)
    except Exception as e:
        print(f"Error fetching Spotify token or user info: {e}")
        return redirect("/")

    message = None
    playlists = []

    if request.method == "POST":
        func = request.form.get("function")

        if func == "sort":
            try:
                total = int(request.form.get("total", 10))
                playlist = request.form.get("playlist")
                sort(sp, total, playlist)
                message = "Sorting complete!"
            except Exception as e:
                message = f"Error during sorting: {e}"

        elif func == "clear":
            try:
                clear_playlists(sp)
                message = "Playlists cleared!"
            except Exception as e:
                message = f"Error during clearing playlists: {e}"

        elif func == "top20":
            try:
                time_range = request.form.get("timeRange")
                top20_songs(sp, time_range)
                message = "Top 20 songs playlist created!"
            except Exception as e:
                message = f"Error creating top 20 songs playlist: {e}"

        elif func == "artistTop":
            try:
                artist = request.form.get("artistName")
                result = artistTop(sp, artist)
                message = result if result else "Artist top songs playlist created!"
            except Exception as e:
                message = f"Error creating artist top songs playlist: {e}"

        elif func == "topArtistsSongs":
            try:
                time_range = request.form.get("timeRange")
                topArtistsSongs(sp, time_range)
                message = "Top artists songs playlist created!"
            except Exception as e:
                message = f"Error creating top artists songs playlist: {e}"

    try:
        playlists = get_all_playlists(sp)
    except Exception as e:
        print(f"Error fetching playlists: {e}")
        playlists = []

    return render_template(
        "Functions/index.html",
        is_logged_in=is_logged_in,
        name=name,
        message=message,
        playlists=playlists
    )

@app.route("/login")
def login():
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    sp_oauth = get_spotify_oauth()
    session.clear()
    code = request.args.get('code')

    if not code:
        return redirect('/')

    try:
        token_info = sp_oauth.get_access_token(code)
    except Exception as e:
        print(f"Error getting access token: {e}")
        return redirect('/')

    session["token_info"] = token_info
    return redirect("/functions")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
