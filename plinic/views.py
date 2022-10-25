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
from .models import Post, Playlist, Notice, Tag, Genre
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


class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        genre_names = [genre.name for genre in genres]
        return Response(genre_names)


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

        # 임의의 유저 5명 생성
        try:
            username_lists = [
                "Lami",
                "taeyoung2da",
                "goddessana",
                "woin2ee",
                "blooper20",
            ]
            for username in username_lists:
                get_user_model().objects.create_user(
                    username=username, password=username
                )
        except:
            pass

        # 임의의 장르 생성
        try:
            for genre_name in [
                "acoustic",
                "blues",
                "classical",
                "jazz",
                "children",
                "disney",
                "hip - hop",
                "rock",
                "j-pop",
                "k-pop",
                "new-age",
                "opera",
                "pop",
                "reggae",
                "tango",
                "techno",
                "singer",
                "songwriter",
                "R & B",
                "british",
                "disco",
                "new - release",
                "movies",
                "soundtracks",
                "edm",
                "sleep",
                "soul",
                "study",
                "summer",
                "road",
                "trip",
                "rainy",
                "day",
                "dance",
                "holidays",
                "party",
                "work",
                "out",
                "sad",
                "romance",
            ]:
                new_genre = Genre(name=genre_name)
                new_genre.save()
        except:
            pass

        # 임의의 플레이리스트 생성
        if Playlist.objects.count() > 0:
            pass
        else:
            playlist_title_list = [
                "🎄 Happy Christmas 🎄",
                "나는 잠이 올것이다",
                "힙합",
                "애플의 광고 음악 같은",
                "짝사랑할 때 듣는 노래",
                "최강 디즈니",
                "🕺🏻딴수딴수🕺🏻",
            ]
            for title in playlist_title_list:
                new_playlist = Playlist(
                    title=title,
                    total_url="https://www.youtube.com/watch?v=hDphjzXZW-4&list=TLGG-gDeQ2YlcRMyNDEwMjAyMg",
                    profile=Profile.objects.first(),
                    genre=random.choice(list(Genre.objects.all())),
                )
                new_playlist.save()

        # 임의의 트랙 생성
        if Track.objects.all().count() > 0:
            pass
        else:
            new_track1 = Track(
                playlist=random.choice(list(Playlist.objects.all())),
                title="영탁(제이심포니) - 너에게 가는 길(20120504 희망TV)",
                url="https://www.youtube.com/watch?v=ihlpYVDUq0w",
                duration=timedelta(seconds=300),
            )
            new_track1.save()
            new_track2 = Track(
                playlist=random.choice(list(Playlist.objects.all())),
                title="[4K] 'Alcohol-Free' The Ellen DeGeneres Show Full Performance",
                url="https://www.youtube.com/watch?v=FRvPXtvfg1w&list=RDGMEM0s70dY0AfCwh3LqQ-Bv1xgVMFRvPXtvfg1w&start_radio=1",
                duration=timedelta(seconds=300),
            )
            new_track2.save()

        # 임의의 게시물 생성
        if Post.objects.count() > 0:
            pass
        else:
            post_list = {
                "크리스마스 노래 듣고 싶지 않으세여!??!??!??": "이제 곧 #크리스마스 잖아여!!!!!!!!!!!! 이 노래 듣고 연말 느낌을 내보자구요 꺄아",
                "💤 잠이 오지 않는 밤": "잠이 오지 않아 #잠이솔솔 #쿨쿨자라 #꿀잠비법",
                "🎶 노동요 추천 | 일할 때 듣는 노래 🎶": "난 이거 틀고 일해 #노동요",
                "Apple CM (Style..) Songs 🍎": "애플의 광고 음악은 굉장합니다.애플이 세계를 지배할 것 입니다.감각적인 플레이리스트 음악을 들어보시죠.",
                "난 선생이고 넌 학생이야": "여러분, #사랑 이란 무엇이라 생각하십니까.??!!!?!?!?!?!? 이뤄지기 힘든 #사랑 을 mu-sic으로 표현해봤읍니다.",
                "디즈니니니": "제가 #디즈니 를 참 좋아하는데요",
                "내가 이 구역의 댄.스.머.신": "이 구역을 접수하러 왔다",
                "외롭게 코딩하고 계신가요?": "외로운 #밤 을 같이 보내 줄 음악 듣고 가시죠. ^^",
            }
            for data in list(post_list.items()):
                new_post = Post(
                    profile=Profile.objects.first(),
                    title=data[0],
                    content=data[1],
                    playlist=random.choice(list(Playlist.objects.all())),
                )
                new_post.save()

        # 임의의 태그 생성
        if Tag.objects.count() > 0:
            pass
        else:
            tag_list = [
                "크리스마스",
                "잠이솔솔",
                "쿨쿨자라",
                "꿀잠비법",
                "노동요",
                "애플",
                "Apple",
                "CM",
                "사랑",
                "디즈니",
            ]
            for name in tag_list:
                new_tag = Tag(name=name)
                new_tag.save()

        # 임의의 공지사항 생성
        if Notice.objects.count() > 0:
            pass
        else:
            notice_list = {
                "[Plinic] 서버 정기점검 안내": "오늘 오전 3시부터 11시까지 서버 정기점검이 있을 예정입니다.",
                "[Plinic] 커뮤니티 공지사항입니다.": "제발 가입 좀 해 주세요. 감사합니다.",
                "[Plinic] 악성 유저 강제탈퇴 안내": "악성 유저는 운영진에서 모니터링 후 경고, 강제탈퇴 예정입니다.",
                "[Plinic] 데이터 센터 화재 이슈로 인한 서비스 에러 안내": """화재 사고 발생 직후부터 모든 카카오 임직원은 서비스 정상화를 위해 총력을 다하고 있습니다. 현재 대부분의 서비스가 정상화됐습니다. 저희의 준비 및 대응 상황이 이용자분들의 기대에 미치지 못해 장시간 동안 큰 불편을 드렸습니다.
                지난 주말, 소통에 불편을 겪으셨을 이용자분들, 택시 호출을 받지 못한 기사님, 광고 채널을 이용하지 못하신 사장님 등 카카오 서비스를 이용하고 계신 이용자와 파트너분들을 생각하면 더욱 마음이 무거워집니다.
                잃어버린 신뢰를 회복하는데 그 어느 때보다 크고 오랜 노력이 필요하다는 것을 알고 있습니다. 이번 일을 계기로 카카오 전체의 시스템을 점검하고 쇄신하겠습니다. 이용자분들께서 다시 안심하고 편리하게 카카오 서비스를 사용하실 수 있는 환경을 구축하고, 이용자 여러분의 신뢰를 회복하기 위해 최선의 노력을 다하겠습니다.
                관계 당국의 우려 역시 어느 때보다 무겁게 받아들이며, 조사와 요청에 성실하게 협조하겠습니다. 모든 서비스가 정상화되는 대로 이번 사건에 대해 원인을 철저히 규명하고, 이러한 일이 또다시 발생하지 않도록 최대한의 조치를 취해 나갈 것을 약속드립니다.
                마지막으로 말씀드리겠습니다. 저는 카카오의 서비스를 책임지는 각자 대표로서 그 어느 때보다 참담한 심정과 막중한 책임을 통감하며, 카카오의 쇄신과 변화에 대한 의지를 다지고자 대표이사직을 내려놓고, 이번 사태에 끝까지 책임을 지고자 비상대책위원회 재발방지소위를 맡아, 부족한 부분과 필요한 부분을 채워나가는 일에만 전념하겠습니다. 
                나아가 카카오뿐만 아니라, 대한민국 IT 업계 전반에 이와 같은 일들이 일어나지 않게, 작게나마 도움이 될 수 있도록 이번 사건이 마무리될 때까지 더욱 무거운 책임감으로 임하겠습니다.
                우리뿐 아니라 업계 전체의 재발을 방지하려면 스스로의 치부를 드러내야 할 수도 있습니다. 하지만 이것도 카카오의 의무라고 생각합니다. '모든 항공 규정은 피로 쓰였다'라는 말이 있습니다. 이는 비행을 하며 일어난 수많은 사고와 사례 공유를 통해 좀 더 안전한 하늘길이 이뤄졌다는 뜻입니다. 우리 IT 산업도 이 길을 갔으면 합니다.\
                이번 기회를 통해 처절하게 반성하고 사회에 공유하며 마지막 소임을 다하고자 합니다.""",
            }

            for data in notice_list.items():
                new_notice = Notice(
                    author=Profile.objects.first(),
                    title=data[0],
                    content=data[1],
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
