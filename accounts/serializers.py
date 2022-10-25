from rest_framework import serializers
from .models import Profile


class PublicProfilePageSerializer(serializers.ModelSerializer):
    """
    자신의 마이페이지에 접근했을 때
    내 공개 / 비공개 플레이리스트
    내가 스크랩한 플레이리스트
    """

    profile_img = serializers.ImageField(source="profile_pic")
    written_posts = serializers.SerializerMethodField()
    public_playlists = serializers.SerializerMethodField()
    scrapped_playlists = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "nickname",
            "profile_img",
            "public_playlists",
            "scrapped_playlists",
            "written_posts",
        ]

    def get_written_posts(self, obj):
        posts = obj.post_set.all()
        posts_info = [
            {"id": posts.id, "title": posts.title, "content": posts.content}
            for posts in posts
        ]
        return posts_info

    def get_public_playlists(self, obj):
        playlists = obj.playlist_profile_set.filter(is_public=True)
        playlists_info = [
            {
                "title": playlist.title,
                "thumbnail": playlist.thumbnail.url,
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


class PrivateProfileSerializer(PublicProfilePageSerializer):
    class Meta:
        model = Profile
        fields = [
            "nickname",
            "profile_img",
            "public_playlists",
            "private_playlists",
            "written_posts",
        ]

    written_posts = serializers.SerializerMethodField()
    private_playlists = serializers.SerializerMethodField()
    scrapped_playlists = serializers.SerializerMethodField()

    def get_private_playlists(self, obj):
        playlists = obj.playlist_profile_set.filter(is_public=False)
        playlists_info = [
            {
                "title": playlist.title,
                "thumbnail": playlist.thumbnail.url,
                "id": playlist.id,
            }
            for playlist in playlists
        ]
        return playlists_info

    def get_written_posts(self, obj):
        posts = obj.post_set.all()
        posts_info = [
            {"id": posts.id, "title": posts.title, "content": posts.content}
            for posts in posts
        ]
        return posts_info

    def get_scrapped_playlists(self, obj):
        playlists = obj.playlist_scrapper_set.all()
        playlists_info = [
            {"title": playlist.title, "id": playlist.id} for playlist in playlists
        ]
        return playlists_info


class AuthorSerializer(PublicProfilePageSerializer):
    class Meta:
        model = Profile
        fields = ["id", "nickname", "profile_img"]
