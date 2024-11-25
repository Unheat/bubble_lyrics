import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
# Spotify API credentials
load_dotenv("api.env")
REDIRECT_URI = "http://localhost:8080"
CLIENT_ID = os.getenv("SPO_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPO_CLIENT_SECRET")
print(CLIENT_ID, CLIENT_SECRET)  # Debug: Check value

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing"
))

def get_current_song():
    """
    Fetch the currently playing song's title, artist, and progress.
    """
    current_track = sp.current_user_playing_track()
    if current_track:
        song_title = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        progress_ms = current_track['progress_ms']
        duration_ms = current_track['item']['duration_ms']
        return {
            "title": song_title,
            "artist": artist_name,
            "progress_ms": progress_ms,
            "duration_ms": duration_ms
        }
    return None
if __name__ == "__main__":
    print(get_current_song())