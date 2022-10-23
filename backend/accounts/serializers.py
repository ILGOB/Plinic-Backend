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

    class Meta:
        model = Profile
        fields = ["nickname", "profile_img", "my_playlists", "scrapped_playlists"]

    def get_my_playlists(self, obj):
        playlists = obj.playlist_profile_set.all()
        playlists_info = [
            {"title": playlist.title, "id": playlist.id} for playlist in playlists
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
