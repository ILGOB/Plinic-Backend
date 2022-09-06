from googleapiclient.errors import HttpError
from .utils import playlist_maker as pl
from rest_framework import status, generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .models import Playlist
from .models import Genre
from .serializers import PostSerializer
from .serializers import PlaylistSerializer


global total_urls
total_urls = ""

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


class RandomPlayListView(APIView):
   
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
                json_val = pl.random_playlist(genre, num)
                ResponseData = Response(json_val)
                
                total_urls = json_val["Total_urls"]
                print(total_urls)
                
                print(type(request.user.profile))
                #개선이 매우 매우 매우 필요함!!!!!!
                PlaylistGenre = list(Genre.objects.all())

                for listgenre in PlaylistGenre:
                    if "<Genre : "+genre+">" == str(listgenre):
                        indexGenre = PlaylistGenre.index(listgenre)
                        
                RandomPlayList = Playlist()
                RandomPlayList.title = "tempList"
                RandomPlayList.total_url = json_val["Total_urls"]            
                RandomPlayList.profile = request.user.profile
                RandomPlayList.genre = PlaylistGenre[indexGenre]

                
                RandomPlayList.save()

                return ResponseData
        # watch_videos?video_ids=

random_play_list_view = RandomPlayListView.as_view()