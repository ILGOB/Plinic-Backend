from . import get_recommendations as spotty
from . import youtube as yt
from . import youtube_duration as yd

import requests
from rest_framework.response import Response


def random_playlist(genre, num):
    get_namelist = spotty.get_recommendation_name(genre, num)  # 얕은카피

    counter = 1

    #key = artist, value = title
    namelist_keys = get_namelist.keys()
    list_by_urls = []
    songList = []
    list_by_dict = dict()

    # print(get_namelist)
    # print(namelist_keys)

    for i in namelist_keys:
        tempdict = dict()

        # key값인 아티스트의 이름과 value인 노래 제목을 더하여 검색
        temp = yt.youtube_search_list(get_namelist[i] + " " + i)
        tempList = list(map(str, temp.split()))

        # 제목을 songList에 담음
        # songList.append(get_namelist[i])
        # songList.append(tempList[-1])
        tempdict["title"] = get_namelist[i]

        # id 분리 완료
        tempList = list(map(str, tempList[-1].split('/')))
        tempList = list(map(str, tempList[-1].split('=')))

        # string값으로 duration을 반환하는 find_duration 함수
        duration = yd.find_duration(tempList[-1])
        tempdict["url"] = tempList[-1]

        # songList.append(duration)
        tempdict["duration"] = duration
        songList.append((tempdict))

        # 각각 분리된 id들을 임시로 리스트에 담아 저장
        list_by_urls.append(tempList[-1])
        counter += 1

    urls = ",".join(list_by_urls)

    endpoint = 'http://www.youtube.com/watch_videos?video_ids='+urls
    response = requests.get(endpoint)
    urls_by_response = response.url

    list_by_dict["tracks"] = songList
    list_by_dict["Total_urls"] = urls_by_response
    # print(list_by_dict)
    tempurl = list(map(str, urls_by_response.split('list=')))
    # print(tempurl)
    for tempdict in list_by_dict["tracks"]:
        tempdict["url"] = "https://www.youtube.com/watch?v=" + \
            tempdict["url"]+"&list="+tempurl[-1]

    return list_by_dict
