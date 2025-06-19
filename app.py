from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from Main import sort
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'







@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        action = request.form.get('action')
        if action == 'sort':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))

            sp = spotipy.Spotify(auth=token_info['access_token'])
            user_id = sp.current_user()['id']
            message = sort(sp, user_id)
            #message = sp.current_user_saved_tracks(limit=1, offset=0)


        elif action == 'authorization':
            return redirect(url_for('login'))  # Starts login flow

    return render_template("index.html", message=message)

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope = (
            "ugc-image-upload "
            "user-read-recently-played "
            "user-top-read "
            "user-read-playback-position "
            "user-read-playback-state "
            "user-modify-playback-state "
            "user-read-currently-playing "
            "app-remote-control "
            "streaming "
            "playlist-modify-public "
            "playlist-modify-private "
            "playlist-read-private "
            "playlist-read-collaborative "
            "user-follow-modify "
            "user-follow-read "
            "user-library-save "
            "user-library-read "
            "user-read-email "
            "user-read-private "
            "user-read-birthdate "
            "user-library-modify"
        )

    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read"
    )

    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for('index'))





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)