# 파이썬 기본 모듈인 urllib.request를 사용하여 url을 엶
import json
import urllib.request
from googleapiclient.errors import HttpError


def find_duration(video_id):

    list_by_time = []

    # video_id = "3Y0eUYVjhQM"  # 10H9M11S
    # video_id = "1IlTeOMCNJU"  # 4M31S

    api_key = "AIzaSyCbSm4vQcnvyL1uWHY7dHa95M0TJeiHGPg"
    searchUrl = "https://www.googleapis.com/youtube/v3/videos?id=" + \
        video_id+"&key="+api_key+"&part=contentDetails"
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data = data['items']
    contentDetails = all_data[0]['contentDetails']
    duration = contentDetails['duration']

    # 원물 형태인 PT23H59M1S 형태를 정제

    duration = str(duration)
    duration = duration.lstrip("PT")

    if "H" in duration:
        tempList = list(map(str, duration.split("H")))
        list_by_time.append(tempList[0])
        duration = duration.lstrip(tempList[0])
        duration = duration.lstrip("H")

    if "M" in duration:
        tempList = list(map(str, duration.split("M")))
        list_by_time.append(tempList[0])
        duration = duration.lstrip(tempList[0])
        duration = duration.lstrip("M")

    if "S" in duration:
        tempList = list(map(str, duration.split("S")))
        list_by_time.append(tempList[0])

    for i in list_by_time:
        if len(i) == 1:
            list_by_time[list_by_time.index(
                i)] = "0"+list_by_time[list_by_time.index(i)]

    if len(list_by_time) == 1:
        total_duration = "00:00:{}".format(list_by_time[0])
    elif len(list_by_time) == 2:
        total_duration = "00:{}:{}".format(list_by_time[0], list_by_time[1])
    else:
        total_duration = "{}:{}:{}".format(
            list_by_time[0], list_by_time[1], list_by_time[2])

    return total_duration


if __name__ == "__main__":
    try:
        # pprint.pprint(youtube_search_list("원더풀"))
        print(find_duration("3Y0eUYVjhQM"))
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
