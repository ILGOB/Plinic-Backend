import profile
import sys
sys.path.append("..")

from urllib import request
from googleapiclient.errors import HttpError
from .utils import playlist_maker as pl
from rest_framework import status, generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

import json

from .models import Post, Track, Playlist, Genre

from accounts.models import Profile
from .serializers import PostSerializer

from datetime import timedelta

PlaylistUser = list(Profile.objects.filter(id = 1))
global profile_id
profile_id = PlaylistUser[0]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
        return super().perform_create(serializer)

class RandomPlaylistCreate(APIView):

    def get(self, request):
        if not 'genre' in request.GET or not 'num' in request.GET:
            return Response({"error": "A 'genre' and 'num' is required."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # 장르가 우리가 지정한 장르가 아닐경우 오류메세지 출력
            # 대소문자 구분 없이 정확히 일치하는 데이터 찾기
            # if not plinic.objects.get(name__iexact="request.GET['genre']"):
            #     return Response("This genre is not on the list.")
            # else:
            #     genre = request.GET['genre']
            genre = request.GET['genre']
            # 노래의 개수가 20개 이상일경우 오류메세지 출력
            num = request.GET['num']
            if int(num) >= 21:
                return Response({"error": "More than 20 songs are not possible."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = pl.random_playlist(genre, num)
                data["profile_id"] = request.user.profile.id

                ResponseData = Response(data)
                print(request.user.profile.id)
                

                return ResponseData
    
    def post(self, request):
        data = json.loads(request.body)
        Response_json = Response(data)
        
        print(data["tracks"][0]["title"])



        #######임시 플레이리스트 생성 시작
        #랜덤플레이리스트를 만들어낸 유저의 id정보
        PlaylistUser = list(Profile.objects.filter(id = data["profile_id"]))
    
        # print(PlaylistUser[0])
        # print(type(PlaylistUser[0]))
        # print(type(request.user.profile))
        #테스트용으로 만든 변수
        titleName = "title123414"

        #개선이 매우 매우 매우 필요함!!!!!!
        #랜덤 플레이리스트의 장르가 설정한 장르와 맞을때만 작동하도록 else문을 작성해야함
        #filter로 안한 이유는 작성시 filter를 제대로 몰라서, 수정가능함 
        PlaylistGenre = list(Genre.objects.all())

        for listgenre in PlaylistGenre:
            if "<Genre : "+data["Genre"]+">" == str(listgenre):
                indexGenre = PlaylistGenre.index(listgenre)
                
        RandomPlayList = Playlist()
        RandomPlayList.title = titleName
        RandomPlayList.total_url = data["Total_urls"]            
        RandomPlayList.profile = PlaylistUser[0]
        RandomPlayList.genre = PlaylistGenre[indexGenre]
        
        RandomPlayList.save()
        ######임시 플레이리스트 생성 완료

        ######Track생성 시작
        RandomPlayList = list(Playlist.objects.filter(title = titleName).filter(profile = PlaylistUser[0]))
        print(RandomPlayList[0])
        print(type(RandomPlayList[0]))

        for tracks in data["tracks"]:
            RandomPlayList_Track = Track()
            RandomPlayList_Track.playlist = RandomPlayList[0]
            RandomPlayList_Track.title = tracks["title"]
            RandomPlayList_Track.url = tracks["url"]
            duration_list = list(map(int, tracks["duration"].split(":")))
            total_seconds = duration_list[0]*3600+duration_list[1]*60+duration_list[2]
            RandomPlayList_Track.duration = timedelta(seconds = total_seconds)

            RandomPlayList_Track.save()

        nowPlaylist = Playlist.objects.filter(title = titleName).filter(profile = PlaylistUser[0])
        for qs in nowPlaylist:
            print("id:{id}, title: {title}".format(**qs.__dict__))
        nowPlaylist.update(title = "포스트로 받아온 타이틀이름3!")

        # RandomPlayList = Playlist.objects.filter(title = "tempList").filter(profile = PlaylistUser[0])
        
        return Response_json
        
random_play_list_create = RandomPlaylistCreate.as_view()

class PlaylistDetail(APIView):
    def put(self, request, **kwargs):
        id = kwargs.get("id")
        #profile 나중에 request.user.profile로 바꿔야함
        Playlist.objects.filter(id = id).filter(profile = profile_id).update(title = "업데이트된 타이틀")
        return Response()
    def delete(self, request, **kwargs):
        id = kwargs.get("id")
        #profile 나중에 request.user.profile로 바꿔야함
        Playlist.objects.filter(id = id).filter(profile = profile_id).delete()
        return Response()
play_list_detail = PlaylistDetail.as_view()


#혹시몰라서 남겨둠, 플레이리스트로 통합됨.
# class RandomPlayListView(APIView):
   
#     def get(self, request):
#         if not 'genre' in request.GET or not 'num' in request.GET:
#             return Response({"error": "A 'genre' and 'num' is required."}, status=status.HTTP_400_BAD_REQUEST)

#         else:
#             # 장르가 우리가 지정한 장르가 아닐경우 오류메세지 출력
#             # 대소문자 구분 없이 정확히 일치하는 데이터 찾기
#             # if not plinic.objects.get(name__iexact="request.GET['genre']"):
#             #     return Response("This genre is not on the list.")
#             # else:
#             #     genre = request.GET['genre']
#             genre = request.GET['genre']
#             # 노래의 개수가 20개 이상일경우 오류메세지 출력
#             num = request.GET['num']
#             if int(num) >= 21:
#                 return Response({"error": "More than 20 songs are not possible."}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 data = pl.random_playlist(genre, num)
#                 data["profile_id"] = request.user.profile.id

#                 ResponseData = Response(data)
#                 print(request.user.profile.id)
                

#                 return ResponseData
#         # watch_videos?video_ids=

# random_play_list_view = RandomPlayListView.as_view()