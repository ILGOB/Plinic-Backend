from googleapiclient.errors import HttpError
from .utils import playlist_maker as pl
from rest_framework import status
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class random_playlist_view(APIView):

    def get(self, request):
        if not 'genre' in request.GET or not 'num' in request.GET:
            return Response("A 'genre' and 'num' is required.", status=status.HTTP_400_BAD_REQUEST)

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
                return Response("More than 20 songs are not possible.", status=status.HTTP_400_BAD_REQUEST)
            else:
                json_val = Response(pl.random_playlist(genre, num))
                return json_val
        # watch_videos?video_ids=