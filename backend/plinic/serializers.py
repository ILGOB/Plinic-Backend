from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Playlist


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return  {"nickname" : obj.profile.nickname, "profile_pic" : obj.profile.profile_pic if obj.profile.profile_pic else "프로필 사진이 없습니다."}

    class Meta:
        model = Post
        fields = "__all__"
