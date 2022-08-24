import pprint
import requests
from .spotify_settings import headers

'''
genre, limit 을 받아 genre에 맞는 limit 개수만큼의 곡과 artist name 을 반환
딕셔너리로 해도 좋을 것 같아요!
{"track_name" : "아리랑, "artist_name" : "신원미상" }
ㄴ 이런식으로..?
'''


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
        # pprint.pprint(f'Track name : {track_name}')
        # pprint.pprint(f'Artirst Name : {artist_name}')
        # pprint.pprint("-"*100)

        outPut.setdefault(artist_name, track_name)
        # print(outPut)
    return outPut


if __name__ == "__main__":
    print(get_recommendation_name("happy", 3))


# get_recommendation_name("rock", 5)
