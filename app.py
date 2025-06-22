from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from Main import sort, clear_playlists, top20_songs, artistTop, testing
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
    return token_info




@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        action = request.form.get('action')
        if action == 'sort':
            selected_Songs = request.form.get('numSort')
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))

            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            user_id = sp.current_user()['id']
            sort(sp, user_id, int(selected_Songs))
            message = "Your liked songs have been sorted and added to the playlists."
        elif action == 'clear':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            clear_playlists(sp)
            message = "All playlists have been cleared."
        elif action == 'top20_songs':
            selected_time = request.form.get('time')
            print("Selected time:", selected_time)  # Debug

            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)

            top20_songs(sp, selected_time)
            message = "Top 20 songs playlist has been created."
        elif action == 'top10_artist':
            selected_artist = request.form.get('artist')
            print("Selected artist:", selected_artist)
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            message = artistTop(sp, selected_artist)
        elif action == 'test':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))
            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'], requests_timeout=30)
            message = testing(sp)
        
            

        

    return render_template("index.html", message=message)

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
    return redirect(url_for('index'))





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)