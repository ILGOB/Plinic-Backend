import base64
import json
from pathlib import Path
import os
import environ
import requests

# load .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# api key
CLIENT_ID = env("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = env("SPOTIFY_CLIENT_SECRET")
ENDPOINT = "https://accounts.spotify.com/api/token"

encoded = base64.b64encode("{}:{}".
                           format(CLIENT_ID, CLIENT_SECRET).
                           encode('utf-8')).decode('ascii')
headers = {"Authorization": "Basic {}".format(encoded)}
payload = {"grant_type": "client_credentials"}
response = requests.post(ENDPOINT, data=payload, headers=headers)
access_token = json.loads(response.text)['access_token']
headers = {"Authorization": "Bearer {}".format(access_token)}


def get_recommendation_tracks(genre, limit):
    """
    장르와 곡 개수를 받아, spotify API 로부터 그것에 맞는 데이터를 리턴
    :param genre: 찾고자 하는 장르
    :param limit: 찾고자 하는 곡의 개수
    :return: {artist_name: blabla, 'track_title': blabla} 형태의 dictionary 를 담고 있는 list 반환

         [{'artist_name': 'Lena Park', 'track_title': '나는 작사가다 Season 01'},
          {'artist_name': '5tion', 'track_title': '우리 결혼까지 하자'},
          {'artist_name': 'Hwaii', 'track_title': '티켓 두장 주세요'}]
    """

    get_recommendations_params = {
        "seed_genres": genre,
        "limit": limit
    }

    response = requests.get("https://api.spotify.com/v1/recommendations", params=get_recommendations_params,
                            headers=headers).json()

    track_with_artist_dict = {}
    track_with_artist_list = []

    for i in range(len(response['tracks'])):
        track_title = response['tracks'][i]['album']['name']
        artist_name = response['tracks'][i]['album']['artists'][0]['name']
        track_with_artist_dict["artist_name"] = artist_name
        track_with_artist_dict["track_title"] = track_title
        new_dict = track_with_artist_dict.copy()
        track_with_artist_list.append(new_dict)

    return track_with_artist_list


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_recommendation_tracks('k-pop', 5))
