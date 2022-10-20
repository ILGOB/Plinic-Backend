import json
from datetime import timedelta
from urllib import request

import random

import requests
from django.shortcuts import redirect
from googleapiclient.errors import HttpError
from requests.auth import HTTPBasicAuth

from accounts.models import Profile
from .permissions import PostPermission
from .utils import playlist_maker as pl
from rest_framework import status, generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post, Track, Playlist, Notice
from .serializers import PostListSerializer, PostDetailSerializer
from .serializers import PlaylistSerializer, NoticeDetailSerializer, NoticeListSerializer, NoticeRecentSerializer


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('recent', '')
        if search == "true":
            self.pagination_class = None
            latest_pk = Notice.objects.last().pk
            qs = Notice.objects.filter(pk=latest_pk)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)
        return super().perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": f"게시물이 성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    action_serializers = {
        # Detail serializers
        'retrieve': NoticeDetailSerializer,
        'update': NoticeListSerializer,
        'delete': NoticeListSerializer,
        # List serializers
        'list': NoticeListSerializer,
        'create': NoticeListSerializer,
        # Recent serailizer
        'recent': NoticeRecentSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.request.query_params.get('recent', ''):
                return self.action_serializers.get('recent', self.serializer_class)
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(NoticeViewSet, self).get_serializer_class()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by("-pk")
    serializer_class = PostDetailSerializer

    # permission_classes = (PostPermission,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
        return super().perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": f"게시물이 성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    action_serializers = {
        'retrieve': PostDetailSerializer,
        'list': PostListSerializer,
        'create': PostListSerializer,
        'update': PostListSerializer,
        'delete': PostListSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(PostViewSet, self).get_serializer_class()


class RandomPlayListView(APIView):
    """
    랜덤 플레이리스트 조회 기능
    """

    def get(self, request):
        if ('genre' not in request.GET) or ('num' not in request.GET):
            # 'genre', 'num' 이 querystring 으로 안 들어오면 에러 메시지 출력
            return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # TODO : 장르가 우리가 지정한 장르가 아닐경우 오류메세지 출력
            genre = request.GET['genre']
            num = request.GET['num']
            if int(num) >= 21:
                return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                json_val = pl.get_random_playlist(genre, num)
                return Response(json_val)


class PlaylistViewSet(ModelViewSet):
    """
    list 에 대한 GET, POST (목록 조회 및 생성)
    detail 에 대한 GET, PUT, DELETE (상세 플레이리스트 조회, 수정, 삭제)
    수정은 "제목" 만 가능해야 함.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class RandomBackgroundView(APIView):
    def get(self, request):
        id_list = ["3116500",
                   "3116506",
                   "5197762",
                   "2697038",
                   "3211457",
                   "857136",
                   "2962724"]
        url = "https://api.pexels.com/videos/videos/"
        api_key = '563492ad6f91700001000001f4e83ff4703f4a20a5a558a554e11d9f'

        headers = {
            'Content-type': 'application/json',
            'Authorization': api_key
        }

        id = random.choice(id_list)
        response = requests.get(url=url + id, headers=headers).json()['video_files']
        print(response)
        return Response({"background_url": response[0]['link']})


class RandomThumbnailView(APIView):
    def get(self, request):
        url = "https://source.unsplash.com/random"
        result_url = requests.get(url)
        return Response({"img_url": result_url.url})


class LikeView(APIView):
    """
    { "post_id" = 1 }
    만 들어온다고 가정
    post() -> 좋아요 추가
    delete() -> 좋아요 취소
    """

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.liker_set.add(request.user.profile)
        return Response(post.liker_set.count())

    def delete(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.liker_set.remove(request.user.profile)
        return Response(post.liker_set.count())
