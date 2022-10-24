from rest_framework import serializers
from .models import Profile


class ProfilePageSerializer(serializers.ModelSerializer):
    """
    내 공개 플레이리스트
    내가 스크랩한 플레이리스트
    """

    profile_img = serializers.ImageField(source="profile_pic")
    my_playlists = serializers.SerializerMethodField()
    scrapped_playlists = serializers.SerializerMethodField()
    my_posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "nickname",
            "profile_img",
            "my_playlists",
            "scrapped_playlists",
            "my_posts",
        ]

    def get_my_posts(self, obj):
        posts = obj.post_set.all()
        posts_info = [
            {"id": posts.id, "title": posts.title, "content": posts.content}
            for posts in posts
        ]
        return posts_info

    def get_my_playlists(self, obj):
        playlists = obj.playlist_profile_set.all()
        playlists_info = [
            {
                "title": playlist.title,
                "thumbnail": playlist.thumbnail,
                "id": playlist.id,
            }
            for playlist in playlists
        ]
        return playlists_info

    def get_scrapped_playlists(self, obj):
        playlists = obj.playlist_scrapper_set.all()
        playlists_info = [
            {"title": playlist.title, "id": playlist.id} for playlist in playlists
        ]
        return playlists_info


class AuthorSerializer(ProfilePageSerializer):
    class Meta:
        model = Profile
        fields = ["id", "nickname", "profile_img"]
