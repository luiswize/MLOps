import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from pprint import pprint
import json
import pandas as pd

with open("secrets.txt") as f:
    secret_ls = f.readlines()
    cid = secret_ls[0]
    secret = secret_ls[1]


def spotipy_authorize(cid: str, secret: str):
    client_credentials_manager = SpotifyClientCredentials(cid, secret)
    return spotipy.Spotify(client_credentials_manager)


sp = spotipy_authorize(cid, secret)

# playlist_link = "https://open.spotify.com/playlist/1fK9MFZlxbHoPPifTW1KJs?si=c0c6faf280ed411a"
playlist_link = "https://open.spotify.com/playlist/0HGQL3BVdLbShIpTtqTQvX?si=b006dcda4b6e4091"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
print(playlist_URI)


test = sp.playlist_items(playlist_URI)
print(test)


track_urs = []
track_names = []
release_dates = []
artists_info = []
artist_names = []
artist_pops = []
artists_genres = []
albums = []
tracks_pop = []

for track in sp.playlist_items(playlist_URI)["items"]:
    track_uri = track["track"]["uri"]
    track_urs.append(track_uri)

    track_name = track["track"]["name"]
    track_names.append(track_name)

    release_date = track["track"]["album"]["release_date"]
    release_dates.append(release_date)

    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    artists_info.append(artist_info)

    artist_name = track["track"]["artists"][0]["name"]
    artist_names.append(artist_name)

    artist_pop = artist_info["popularity"]
    artist_pops.append(artist_pop)

    artist_genres = artist_info["genres"]
    artists_genres.append(artist_genres)

    album = track["track"]["album"]["name"]
    albums.append(album)

    track_pop = track["track"]["popularity"]
    tracks_pop.append(track_pop)



data = {
    "track_urs": track_urs,
    "track_names": track_names,
    "release_dates": release_dates,
    "artists_info": artists_info,
    "artist_names": artist_names,
    "artist_pops": artist_pops,
    "artists_genres": artists_genres,
    "albums": albums,
    "tracks_pop": tracks_pop
}


df = pd.DataFrame(data)
print(df.head())
# df.to_csv('SUCCESS.csv')



