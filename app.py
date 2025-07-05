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


nmae = None


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
    return token_info

sp = None

#playlist = ["chuj", "chuj2", "chuj3", "chuj4", "chuj5", "chuj6", "chuj7", "chuj8", "chuj9", "chuj10"]

    

@app.route("/")
def main():
    is_logged_in = "token_info" in session
    return render_template("Main/index.html", is_logged_in=is_logged_in)

@app.route("/functions", methods=["GET", "POST"])
def functions():
    global name
    global playlists
    message = None
    token_info = session.get("token_info", None)

    if not token_info:
        return redirect(url_for('login'))

    # Refresh token if expired
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)

    name = getName(sp)


    # ✅ Now you can safely fetch playlists
    playlists = get_all_playlists(sp)

    if request.method == "POST":
        
        action = request.form.get('action')
        if action == 'sort':

            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            selected_Songs = request.form.get('numSort')
            selected_playlist = request.form.get("selected_option")
            sort(sp, int(selected_Songs), selected_playlist)
            message = "Your liked songs have been sorted and added to the playlists."
            playlists = get_all_playlists(sp)
        elif action == 'clear':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            clear_playlists(sp)
            message = "All playlists have been cleared."
            playlists = get_all_playlists(sp)
        elif action == 'top20_songs':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            selected_time = request.form.get('time')
            top20_songs(sp, selected_time)
            message = "Top 20 songs playlist has been created."
            playlists = get_all_playlists(sp)
        elif action == 'top10_artist':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            selected_artist = request.form.get('artist')
            message = artistTop(sp, selected_artist)        
            playlists = get_all_playlists(sp)
        elif action == 'topArtistsSongs':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            selected_time = request.form.get('time')
            topArtistsSongs(sp, selected_time)
            playlists = get_all_playlists(sp)
        
            

        
            

        
    is_logged_in = "token_info" in session


    return render_template("Functions/index.html", message=message, my_list=playlists, is_logged_in=is_logged_in, name=name)


@app.route('/help')
def help_page():
    is_logged_in = "token_info" in session
    return render_template("Help/index.html", is_logged_in=is_logged_in)

@app.route('/about')
def about_page():
    is_logged_in = "token_info" in session
    return render_template('About/index.html', is_logged_in=is_logged_in)

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
    return redirect(url_for('main'))  # Redirect to home or login page




@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative user-top-read"
    )

    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info
    return redirect(url_for('main'))





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)