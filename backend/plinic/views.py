import random
from datetime import timedelta

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Profile
from .models import Post, Playlist, Notice
from .serializers import (
    PlaylistSerializer,
    NoticeDetailSerializer,
    NoticeListSerializer,
    NoticeRecentSerializer,
)
from .serializers import PostListSerializer, PostDetailSerializer
from .utils import playlist_maker as pl


class NoticeViewSet(ModelViewSet):
    """
    공지사항을 처리하는 APIView

    공지사항 관련 권한 설정:
        GET     : 로그인된 모든 유저
        POST    : 모든 관리자
        PUT     : 모든 관리자
        DELETE  : 모든 관리자
    """

    queryset = Notice.objects.all()
    serializer_class = NoticeDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        recent = self.request.query_params.get("recent", "")
        if recent == "true":
            self.pagination_class = None
            latest_pk = Notice.objects.last().pk
            qs = Notice.objects.filter(pk=latest_pk)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)
        return super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        serializer = self.get_serializer(data=data)
        recent = self.request.query_params.get("recent", "")
        if recent == "true":
            data = super(NoticeViewSet, self).list(request=request).data[0]
            return Response(data)
        return super(NoticeViewSet, self).list(request=request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": f"게시물이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )

    action_serializers = {
        # Detail serializers
        "retrieve": NoticeDetailSerializer,
        "update": NoticeListSerializer,
        "delete": NoticeListSerializer,
        # List serializers
        "list": NoticeListSerializer,
        "create": NoticeListSerializer,
        # Recent serailizer
        "recent": NoticeRecentSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            if self.request.query_params.get("recent", ""):
                return self.action_serializers.get("recent", self.serializer_class)
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(NoticeViewSet, self).get_serializer_class()


class PostViewSet(ModelViewSet):
    """
    게시물을 처리하는 APIView

    공지사항 관련 권한 설정:
        GET     : 로그인된 모든 유저
        POST    : 로그인된 모든 유저
        PUT     : 로그인 된, 게시물의 저자 본인만
        DELETE  : 로그인 된, 게시물의 저자 본인만

    """

    queryset = Post.objects.all().order_by("-pk")
    serializer_class = PostDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
        return super().perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"success": f"게시물이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )

    action_serializers = {
        "retrieve": PostDetailSerializer,
        "list": PostListSerializer,
        "create": PostListSerializer,
        "update": PostListSerializer,
        "delete": PostListSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(PostViewSet, self).get_serializer_class()


class LikeView(APIView):
    """
    게시물 좋아요/ 좋아요 취소를 처리하는 APIView

    게시물 좋아요/ 좋아요 취소 관련 권한 설정:
        PUT     : 로그인 된 모든 유저
        DELETE  : 로그인 된 모든 유저

    """

    def put(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.liker_set.add(request.user.profile)
        return Response(
            {
                "success": f"{post_id}번 게시물에 좋아요를 눌렀습니다.",
                "liker_count": post.liker_set.count(),
            }
        )

    def delete(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.liker_set.remove(request.user.profile)
        return Response(
            {
                "success": f"{post_id}번 게시물에 좋아요를 취소했습니다.",
                "liker_count": post.liker_set.count(),
            }
        )


class RandomPlayListView(APIView):
    """
    랜덤 플레이리스트 조회를 처리하는 APIView

    랜덤 플레이리스트 조회 관련 권한 설정:
        GET     : 로그인된 모든 유저
    """

    def get(self, request):
        if ("genre" not in request.GET) or ("num" not in request.GET):
            # 'genre', 'num' 이 querystring 으로 안 들어오면 에러 메시지 출력
            return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # TODO : 장르가 우리가 지정한 장르가 아닐경우 오류메세지 출력
            genre = request.GET["genre"]
            num = request.GET["num"]
            if int(num) >= 21:
                return Response(
                    {"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                json_val = pl.get_random_playlist(genre, num)
                return Response(json_val)


class PlaylistListView(ListAPIView):
    def get_queryset(self):
        profile = Profile.objects.get(nickname=self.kwargs["nickname"])
        qs = Playlist.objects.filter(profile=profile)
        return qs

    serializer_class = PlaylistSerializer


class ScrapView(APIView):
    """
    특정 플레이리스트의 스크랩, 스크랩 취소를 처리하는 APIView

    스크랩에 대한 권한 설정 :
        PUT     : 로그인 된 모든 유저
        DELETE  : 로그인 된 모든 유저
    """

    def put(self, request, playlist_id):
        """플레이리스트를 스크랩 목록에 추가"""
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist.scrapper_set.add(request.user.profile)
        scrapped_playlists_qs = request.user.profile.playlist_scrapper_set.all()
        scrapped_playlists_names = [
            playlist.title for playlist in scrapped_playlists_qs
        ]
        return Response(
            {
                "success": "플레이리스트 '{}' 를 스크랩했습니다. ".format(playlist.title),
                "scrapped_playlists": scrapped_playlists_names,
            }
        )

    def delete(self, request, playlist_id):
        """플레이리스트를 스크랩 목록에서 제거"""
        playlist = Playlist.objects.get(pk=playlist_id)
        playlist.scrapper_set.remove(request.user.profile)
        scrapped_playlists_qs = request.user.profile.playlist_scrapper_set.all()
        scrapped_playlists_names = [
            playlist.title for playlist in scrapped_playlists_qs
        ]
        return Response(
            {
                "success": "플레이리스트 '{}' 를 스크랩 취소했습니다. ".format(playlist.title),
                "scrapped_playlists": scrapped_playlists_names,
            }
        )


class DummyDataView(APIView):
    def get(self, request):
        from plinic.models import Genre, Playlist, Track, Post, Tag
        from django.contrib.auth import get_user_model
        import time

        # 임의의 유저 생성
        try:
            user1 = get_user_model().objects.create_user(
                username="dummy", password="dummy"
            )
            user2 = get_user_model().objects.create_user(
                username="some_username", password="some_username"
            )
        except:
            pass

        # 임의의 장르 생성
        try:
            for genre_name in ["k-pop", "j-pop", "fuckin-pop", "rock"]:
                new_genre = Genre(name=genre_name)
                new_genre.save()
        except:
            pass

        # 임의의 플레이리스트 생성
        if Playlist.objects.count() > 0:
            pass
        else:
            for i in range(30):
                new_playlist = Playlist(
                    title=f"{i + 1} 번째 플레이리스트 제목 더미 데이터..",
                    total_url="gdsanadev.com",
                    profile=Profile.objects.first(),
                    genre=random.choice(list(Genre.objects.all())),
                )
                new_playlist.save()

        # 임의의 트랙 생성
        if Track.objects.count() > 0:
            pass
        else:
            for i in range(20):
                new_track = Track(
                    playlist=random.choice(list(Playlist.objects.all())),
                    title=f"제목{i + 1} 임........",
                    url="gdsanadev.com",
                    duration=timedelta(minutes=20),
                )
                new_track.save()

        # 임의의 게시물 생성
        if Post.objects.count() > 0:
            pass
        else:
            for i in range(30):
                new_post = Post(
                    profile=Profile.objects.first(),
                    title=f"플리닉 {i + 1} 번째 포스팅.",
                    content=f"플리닉 {i + 1} 번째 포스팅.",
                    playlist=random.choice(list(Playlist.objects.all())),
                )
                new_post.save()

        # 임의의 태그 생성
        if Tag.objects.count() > 0:
            pass
        else:
            for i in range(10):
                new_tag = Tag(name=f"{i + 1}태그")
                new_tag.save()

        # 임의의 공지사항 생성
        if Notice.objects.count() > 0:
            pass
        else:
            for i in range(30):
                new_notice = Notice(
                    author=Profile.objects.first(),
                    title=f"플리닉 {i + 1} 번째 공지사항.",
                    content=f"플리닉 {i + 1} 번째 공지사항인데, 날씨가 춥네요. 얼지 마세요...",
                )
                new_notice.save()

        return HttpResponse("더미 데이터 생성 완료..!")


class RandomBackgroundView(APIView):
    def get(self, request):
        id_list = [
            "3116500",
            "3116506",
            "5197762",
            "2697038",
            "3211457",
            "857136",
            "2962724",
        ]
        url = "https://api.pexels.com/videos/videos/"
        api_key = "563492ad6f91700001000001f4e83ff4703f4a20a5a558a554e11d9f"

        headers = {"Content-type": "application/json", "Authorization": api_key}

        id = random.choice(id_list)
        response = requests.get(url=url + id, headers=headers).json()["video_files"]
        print(response)
        return Response({"background_url": response[0]["link"]})


class RandomThumbnailView(APIView):
    def get(self, request):
        url = "https://source.unsplash.com/random"
        result_url = requests.get(url)
        return Response({"img_url": result_url.url})
