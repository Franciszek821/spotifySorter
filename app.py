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



def get_token():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative"
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

        sort_mode = request.form.get("sortSelect")
        number_value = request.form.get("numberInput")

        if action == 'sort':
            token_info = session.get("token_info", None)
            if not token_info:
                return redirect(url_for('login'))

            token_info = get_token()
            sp = spotipy.Spotify(auth=token_info['access_token'])
            user_id = sp.current_user()['id']
            sort(sp, user_id, number_value)

        elif action == 'authorization':
            print("Authorization button clicked")
            return redirect(url_for('login'))


@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative"
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)



@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public playlist-modify-private user-library-read playlist-read-private playlist-read-collaborative"
    )

    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    session["token_info"] = token_info
    return redirect(url_for('index'))





if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)