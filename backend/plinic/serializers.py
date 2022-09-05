from rest_framework import serializers
from .models import Post, Tag, Playlist, Track
from accounts.serializers import ProfileSerializer


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ["title", "duration", "url"]


class PlaylistSerializer(serializers.ModelSerializer):
    
    track = TrackSerializer(many=True, source="track_set")
    imgUrl = serializers.URLField(source="total_url")
    genre = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Playlist
        fields = ["title", "imgUrl", "thumbnail", "track", "genre"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class PostSerializer(serializers.ModelSerializer):
    isUpdated = serializers.SerializerMethodField()
    created = serializers.DateTimeField(format="%Y.%m.%d", source="created_at")
    updated = serializers.DateTimeField(format="%Y.%m.%d", source="updated_at")
    profile = ProfileSerializer(read_only=True)
    tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name', source="tag_set")
    playlist = PlaylistSerializer(read_only=True)
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
                  "playlist",
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
