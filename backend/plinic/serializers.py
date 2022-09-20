from rest_framework import serializers

from accounts.models import Profile
from .models import Post, Tag, Playlist, Track, Genre
from accounts.serializers import ProfileSerializer


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["title", "duration", "url"]


class PlaylistSerializer(serializers.ModelSerializer):
    track_name = serializers.SlugRelatedField(many=True,
                                              read_only=True,
                                              slug_field='title',
                                              source='track_set')
    track_set = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all(),
                                                   many=True,
                                                   write_only=True)
    imgUrl = serializers.URLField(source="thumbnail")
    totalUrl = serializers.URLField(source="total_url")
    genre_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='genre')
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True)
    scrapper_name_set = serializers.SlugRelatedField(read_only=True, slug_field='nickname', source='scrapper_set', many=True)
    scrapper_id_set = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Profile.objects.all())
    isScrapped = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ["title",
                  "imgUrl",
                  "totalUrl",
                  "track_name",
                  "track_set",
                  "genre_name",
                  "genre_id",
                  "isScrapped",
                  "scrapper_name_set",
                  "scrapper_id_set",]

    def get_isScrapped(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.scrapper_set.filter(pk=user.pk).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    """
    제목
    작성자
    좋아요 여부
    좋아요 수
    생성일자, 수정일자
    태그
    로그인한 유저의 스크랩 여부
    플레이리스트
        장르
    """
    isUpdated = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y.%m.%d", read_only=True, source="created_at")
    updated = serializers.DateTimeField(format="%Y.%m.%d", read_only=True, source="updated_at")
    profile = ProfileSerializer(read_only=True)
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source="tag_set")
    playlistInfo = PlaylistSerializer(read_only=True, source='playlist')
    likerCount = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id",
                  "isUpdated",
                  "created",
                  "updated",
                  "profile",
                  "tag",
                  "playlistInfo",
                  "likerCount",
                  "title",
                  "content",
                  "isLike"]

    def get_likerCount(self, obj):
        return obj.liker_set.count()

    def get_isLike(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.liker_set.filter(pk=user.pk).exists()
        return False

    def get_isUpdated(self, obj):
        created_at = obj.created_at.strftime(format="%Y-%m-%d %H:%M")
        updated_at = obj.updated_at.strftime(format="%Y-%m-%d %H:%M")
        return not updated_at == created_at


class PostListSerializer(serializers.ModelSerializer):
    likerCount = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)
    playListId = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(),
                                                    source='playlist', write_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(many=True,
                                                 queryset=Tag.objects.all(),
                                                 source='tag_set', write_only=True)

    class Meta:
        model = Post
        fields = ["id",
                  "profile",
                  "likerCount",
                  "title",
                  "isLike",
                  # "isScrapped",
                  "tag_ids",
                  "content",
                  "playListId"]

    def get_likerCount(self, obj):
        return obj.liker_set.count()

    def get_isLike(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.liker_set.filter(pk=user.pk).exists()
        return False
