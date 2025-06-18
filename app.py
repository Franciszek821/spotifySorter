from flask import Flask, render_template, request, redirect, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from Main import sort
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'

load_dotenv()





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
            sort(sp, user_id)
            message = "Sorted your liked tracks!"
        elif action == 'authorization':
            return redirect(url_for('login'))  # Starts login flow

    return render_template("index.html", message=message)




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)