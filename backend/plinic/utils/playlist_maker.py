from plinic.utils import get_recommendations as spotty
from plinic.utils import youtube as yt
import requests
from pprint import pprint


def get_random_playlist(genre, num):
    """
    장르와 곡 수를 받아 스포티파이에서 추천하는 음악 리스트 반환
     """

    recommendation_tracks_from_spotty = spotty.get_recommendation_tracks(genre, num)

    # 곡명 + 가수명 을 유튜브 API 를 사용해 검색
    playlist = []
    for i in recommendation_tracks_from_spotty:
        # for single tracks
        search_word = i["artist_name"] + i["track_title"]
        try:
            result = yt.get_youtube_track_data_by_word(search_word)
            result['url'] = requests.get("http://" + result['url']).url
            playlist.append(result)

            # total_url 을 위해서, 유튜브 id 리스트로 바꿈
            # ['cNld-AHw-Wg', 'yAQO1IkSC2U', 'GhEhfOPh00E']
            youtube_id = [data['url'].split('?v=')[1] for data in playlist]
            total_url_before_redirect = 'http://www.youtube.com/watch_videos?video_ids=' + ",".join(youtube_id)
            total_url = requests.get(total_url_before_redirect).url

            return {"tracks": playlist,
                    "total_url": total_url}

        except TypeError as e:
            pass


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_random_playlist('k-pop', 5))
