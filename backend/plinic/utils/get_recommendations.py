import pprint
import requests
from .spotify_settings import headers


def get_recommendation_name(genre, limit):
    get_recommendations_params = {
        "seed_genres": genre,
        "limit": limit
    }
    r = requests.get("https://api.spotify.com/v1/recommendations", params=get_recommendations_params,
                     headers=headers).json()

    outPut = dict()

    for i in range(len(r['tracks'])):
        track_name = r['tracks'][i]['album']['name']
        artist_name = r['tracks'][i]['album']['artists'][0]['name']

        outPut.setdefault(artist_name, track_name)
    return outPut
