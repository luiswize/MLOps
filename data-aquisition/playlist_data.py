import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from credentials import CONFIG
import sys

# CID = CONFIG['cid']
# SECRET = CONFIG['secret']

CID = "da82a340bd1341599bd3c590de6ad9fa"
SECRET = "07c1f564fad9402da3fecc0fa65c0f7b"

# with open("data-aquisition/secrets.txt") as f:
#     secret_ls = f.readlines()
#     cid_test = secret_ls[0]
#     secret_test = secret_ls[1]

def spotipy_authorize(cid: str, secret: str):
    client_credentials_manager = SpotifyClientCredentials(cid, secret)
    return spotipy.Spotify(client_credentials_manager)

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id="da82a340bd1341599bd3c590de6ad9fa", 
        client_secret="07c1f564fad9402da3fecc0fa65c0f7b"
    )
)

# sp = spotipy_authorize(CID, SECRET)


playlist_link = "https://open.spotify.com/playlist/0HGQL3BVdLbShIpTtqTQvX?si=b006dcda4b6e4091"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

def call_playlist(playlist_uri : str, creator='spotify') -> pd.DataFrame:
    

    playlist_features_list = ['artist', 'album', 'track_name', 'track_id','url', 'artist_popularity', 'artist_genre', 'danceability',
                                'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness','instrumentalness', 'liveness', 
                                'valence', 'tempo', 'duration_ms', 'time_signature']
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    artist_df = pd.DataFrame(columns=['artist_popularity', 'artist_genre'])
    
    playlist = sp.user_playlist_tracks(creator, playlist_uri)["items"]
    for track in playlist:
        playlist_features = {}
        artist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        playlist_features["url"] = track['track']['album']['images'][1]['url']
        
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        
        
        artist_features["artist_popularity"] = artist_info["popularity"]
        artist_features["artist_genre"] = str(artist_info["genres"])
        popularity = (artist_info["popularity"])
        genres = str(artist_info["genres"])
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[7:]:
            playlist_features[feature] = audio_features[feature]
            
        # Concat the 
        artist_df = pd.DataFrame(artist_features, index=[0])
        track_df = pd.DataFrame(playlist_features, index = [0])
        
        artist_track_df = pd.concat([track_df, artist_df], axis=1)
        
        playlist_df = pd.concat([playlist_df, artist_track_df], ignore_index = True)
            
    return playlist_df

df = call_playlist(playlist_URI)
print(df.head())