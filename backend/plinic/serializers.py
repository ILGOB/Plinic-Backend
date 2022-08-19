from rest_framework import serializers
from .models import Post, Tag, Playlist
from accounts.serializers import ProfileSerializer


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["title", "url", "thumbnail"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y.%m.%d %H:%M:%S")
    profile = ProfileSerializer(read_only=True)
    tag_set = TagSerializer(many=True)
    playlist = PlaylistSerializer(read_only=True)
    liker_count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id",
                  "created_at",
                  "updated_at",
                  "profile",
                  "tag_set",
                  "playlist",
                  "liker_count",
                  "title",
                  "content",
                  "is_like"]

    def get_liker_count(self, obj):
        return obj.liker_set.count()

    def get_is_like(self, obj):
        if "request" in self.context:
            user = self.context['request'].user
            print(obj.liker_set.filter(pk=user.pk))
            return obj.liker_set.filter(pk=user.pk).exists()
        return False