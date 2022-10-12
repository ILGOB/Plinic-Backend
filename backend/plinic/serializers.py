from rest_framework import serializers

from accounts.models import Profile
from .models import Post, Tag, Playlist, Track, Genre, Notice
from accounts.serializers import ProfileSerializer


class TimeStampedSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y.%m.%d", read_only=True)

    class Meta:
        abstract = True


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
    thumbnail_img_url = serializers.URLField(source="thumbnail")
    total_url = serializers.URLField()
    genre_name = serializers.SlugRelatedField(read_only=True, slug_field='name', source='genre')
    genre_id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), write_only=True)
    scrapper_name_set = serializers.SlugRelatedField(read_only=True, slug_field='nickname', source='scrapper_set',
                                                     many=True)
    scrapper_id_set = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Profile.objects.all())
    is_scrapped = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ["title",
                  "thumbnail_img_url",
                  "total_url",
                  "track_name",
                  "track_set",
                  "genre_name",
                  "genre_id",
                  "is_scrapped",
                  "scrapper_name_set",
                  "scrapper_id_set", ]

    def get_is_scrapped(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.scrapper_set.filter(pk=user.pk).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    name = serializers.SlugField()

    class Meta:
        model = Tag
        fields = ["name", ]


class PostDetailSerializer(TimeStampedSerializer):
    is_updated = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(slug_field='nickname',
                                          read_only=True, source='profile')
    tag_set = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    playlist = PlaylistSerializer(read_only=True)
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["is_updated",
                  "created_at",
                  "updated_at",
                  "tag_set",
                  "playlist",
                  "liker_count",
                  "title",
                  "content",
                  "is_like",
                  "author",]

    def get_liker_count(self, obj):
        return obj.liker_set.count()

    def get_is_like(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.liker_set.filter(pk=user.pk).exists()
        return False

    def get_is_updated(self, obj):
        created_at = obj.created_at.strftime(format="%Y-%m-%d %H:%M")
        updated_at = obj.updated_at.strftime(format="%Y-%m-%d %H:%M")
        return not updated_at == created_at


class NoticeDetailSerializer(TimeStampedSerializer):
    author = serializers.SlugRelatedField(slug_field='nickname',
                                          read_only=True)
    created_at = serializers.DateTimeField(format="%Y.%m.%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y.%m.%d", read_only=True)

    class Meta:
        model = Notice
        fields = ["created_at",
                  "updated_at",
                  "title",
                  "content",
                  "author"]


class NoticeListSerializer(NoticeDetailSerializer, TimeStampedSerializer):
    content = serializers.CharField(write_only=True)

    class Meta:
        model = Notice
        fields = ["title", "author", "content",
                  "created_at", "updated_at"]


class PostListSerializer(serializers.ModelSerializer):
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(read_only=True, slug_field='nickname',
                                          source='profile')
    playlist_id = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(),
                                                     source='playlist', write_only=True)
    tag_set = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                                 many=True, write_only=True)

    class Meta:
        model = Post
        fields = ["author",
                  "liker_count",
                  "title",
                  "is_like",
                  # "isScrapped",
                  "content",
                  "playlist_id",
                  "tag_set", ]

    def get_liker_count(self, obj):
        return obj.liker_set.count()

    def get_is_like(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            return obj.liker_set.filter(pk=user.pk).exists()
        return False
