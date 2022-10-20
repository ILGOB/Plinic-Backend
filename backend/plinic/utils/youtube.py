import json
import os
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import environ
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
검색 단어를 받아 유튜브 링크를 반환
'''
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
DEVELOPER_KEY = env('YOUTUBE_DEVELOPER_KEY')

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_youtube_track_data_by_word(word):
    """
    스포티파이 API 로부터 추천 곡명을 받아온 다음,
    그것 곡명을 토대로 유튜브 API 를 활용하여 유튜브 제목, 곡 이름, 재생시간을 반환한다.
    :param word: 검색 단어
    :return: {'title': '[ENG SUB] [놀면 뭐하니? 후공개] SG워너비 - &#39;아리랑&#39; 풀영상 (Hangout with Yoo - MSG Wannabe YooYaHo)',
              'url': 'youtube.com/watch?v=2M90FlZB8PU'}
    """

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    try:
        search_response = youtube.search().list(type="video",
                                                part="snippet",
                                                q=word,
                                                maxResults=1).execute()
    except HttpError as e:
        print(e)

    try:
        for search_result in search_response.get("items", []):
            video_id = search_result['id']['videoId']
            title = search_result['snippet']['title']
            url = f"youtube.com/watch?v={video_id}"

            url_for_duration = "https://www.googleapis.com/youtube/v3/videos?id=" + video_id + "&key=" + DEVELOPER_KEY + "&part=contentDetails "
            response = urllib.request.urlopen(url_for_duration).read()
            duration_data = json.loads(response)['items'][0]['contentDetails']['duration']

            if 7 < len(duration_data) <= 11 and "H" in duration_data:
                t = datetime.strptime(duration_data, "PT%HH%MM%SS")
                td = timedelta(minutes=t.minute, seconds=t.second).total_seconds()
            elif 5 < len(duration_data) <= 8 and "M" in duration_data:
                t = datetime.strptime(duration_data, "PT%MM%SS")
                td = timedelta(minutes=t.minute, seconds=t.second).total_seconds()
            elif 4 < len(duration_data) <= 5 and "S" in duration_data:
                t = datetime.strptime(duration_data, "PT%SS")
                td = timedelta(minutes=t.minute, seconds=t.second).total_seconds()

            h = str(int(td // 3600)).zfill(2)
            m = str(int((td % 3600) // 60)).zfill(2)
            s = str(int((td % 3600) % 60)).zfill(2)

            duration = f"{h}:{m}:{s}"

            return {"title": title, "url": url, "duration": duration}
    except UnboundLocalError as e:
        pass
