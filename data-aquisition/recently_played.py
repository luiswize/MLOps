import spotipy
from spotipy.oauth2 import SpotifyOAuth



CLIENT_ID = ""
CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = 'https://google.com/'

scope = 'user-read-recently-played'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope
    ) 
)

playlist_link = "https://open.spotify.com/playlist/0HGQL3BVdLbShIpTtqTQvX?si=b006dcda4b6e4091"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
print(playlist_URI)

test = sp.playlist_items(playlist_URI)




def extract (date, limit=50) :
    """Get limit elements from last listen tracks
     Args:
         ds (datetime): : Date to query
         limit (int): Limit of element to query
    """
    breakpoint()
    ds = int (date. timestamp()) * 1000
    return sp.current_user_recently_played(limit=limit, after=ds)
