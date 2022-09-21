import sys
sys.path.append("../spotifyotify_api_web_app")
import authorization
import pandas as pd
from tqdm import tqdm
import time


spotify = authorization.authorize()
genres = spotify.recommendation_genre_seeds()


n_recs = 100

# Initiate a dictionary with all the information you want to crawl
data_dict = {"id":[], "genre":[], "track_name":[], "artist_name":[],
             "valence":[], "energy":[]}

################
## CRAWL DATA ##
################
print('======== working ========')
recs = spotify.recommendations(genres = [genres[0]], limit = n_recs)
print(type(recs))
print(recs)

sys.exit(1)

# Get recs for every genre
for g in tqdm(genres):
    
    # Get n recommendations
    recs = spotify.recommendations(genres = [g], limit = n_recs)
    print(recs)
    # json-like string to dict
    recs = eval(recs.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]
    
    # Crawl data from each track
    for track in recs:
        # ID and Genre
        data_dict["id"].append(track["id"])
        data_dict["genre"].append(g)
        # Metadata
        track_meta = spotify.track(track["id"])
        data_dict["track_name"].append(track_meta.name)
        data_dict["artist_name"].append(track_meta.album.artists[0].name)
        # Valence and energy
        track_features = spotify.track_audio_features(track["id"])
        data_dict["valence"].append(track_features.valence)
        data_dict["energy"].append(track_features.energy)
        
        # Wait 0.2 seconds per track so that the api doesnt overheat
        time.sleep(0.5)
        
##################
## PROCESS DATA ##
##################

# Store data in dataframe
df = pd.DataFrame(data_dict)

# Drop duplicates
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
df.to_csv("valence_arousal_dataset.csv", index = False)
