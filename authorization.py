import tekore as tk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def tekore_authorize():
    app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
    return tk.Spotify(app_token)


def spotipy_authorize():
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager = client_credentials_manager)