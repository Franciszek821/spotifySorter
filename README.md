---

# Spotify Automation Tool

Organize your liked songs and generate custom playlists based on various sorting criteria.
**Note:** Due to Spotify’s policies, this app must be self-hosted. Spotify only allows apps to be published by registered companies.

---

## Running the App

### 1. Creating Your Spotify App

To use the app, you need to create an app on the Spotify for Developers website:
[https://developer.spotify.com](https://developer.spotify.com)

* Log in and click your profile name in the top-right corner to access the **Dashboard**.
* Click **Create an App** and fill in the required information.
* In the **Redirect URIs** section, enter the following:
  `http://127.0.0.1:5000/callback`

### 2. Filling Out the .env File

In the project folder, there is an empty `.env` file. You need to fill it out with the following:

* `SPOTIPY_CLIENT_ID` – Your client ID from Spotify Developer Dashboard
* `SPOTIPY_CLIENT_SECRET` – Your client secret from the same place
* `SPOTIPY_REDIRECT_URI` – Must be exactly: `http://127.0.0.1:5000/callback`
* `FLASK_SECRET_KEY` – A random 32-character string (use a mix of letters, numbers, and symbols)

### 3. Installing Required Libraries

Make sure you have Python and pip installed. Then open a terminal in the project directory (where `requirements.txt` is located) and run:

```
pip install -r requirements.txt
```

### 4. Running the App

To start the app, run the following command in your terminal:

```
python app.py
```

Then open your browser and go to:
`http://127.0.0.1:5000`

---

## App Features

**Sort Playlist**
Sort songs from a playlist or from your liked songs by decade. You can choose how many songs to sort and from which source.

**Delete Playlists**
Delete all playlists that were created by this app.

**Top 20 Songs**
Create a playlist with your top 20 songs. You can select the time range for the ranking.

**Top 10 by Artist**
Generate a playlist of the top 10 songs by a selected artist.

**Top from Top 5 Artists**
Create a playlist featuring the top 10 songs from each of your top 5 favorite artists.

---

App created and developed by Franciszek Domański

I used AI tools such as ChatGPT and GitHub Copilot to help with the code and this README file.
