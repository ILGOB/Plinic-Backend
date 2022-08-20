from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
검색 단어를 받아 유튜브 링크를 반환
'''


DEVELOPER_KEY = "AIzaSyCbSm4vQcnvyL1uWHY7dHa95M0TJeiHGPg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search_list(word):
    '''
    "검색 단어" 를 인자로 받는다.
    최상위에 위치한 비디오 링크를 반환한다.
    '''
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        type="video",
        part="snippet",
        q=word,
        maxResults=1
    ).execute()
    # print(word)
    # print(search_response)

    # ?????여기서 갑자기 None값이 나옴 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ도대체 모르겠네~~도대체 모르겠어~~~~~~~~~
    # 걍 None타입나오면 서치 한번 더 돌리는걸로 하자!
    # split을 돌릴때 none이라 오류나는것이므로, playlistMaker쪽에서 none처리


    # Print the title and ID of each matching resource.
    for search_result in search_response.get("items", []):
        # print(search_result)
        # pprint.pprint(search_result['id']['videoId'])
        # print(f'''{search_result['snippet']['title']}
        # youtube.com/watch?v={search_result['id']['videoId']}''')
        return f'''{search_result['snippet']['title']} 
        youtube.com/watch?v={search_result['id']['videoId']}'''


if __name__ == "__main__":
    try:
        # pprint.pprint(youtube_search_list("원더풀"))
        temp = youtube_search_list(
            "Can Sorry 루미다(Rumeda)")
        print(temp)
        tempList = list(map(str, temp.split()))
        print(tempList[-1])
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
