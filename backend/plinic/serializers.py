from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Playlist


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return  {"nickname" : obj.profile.nickname, "profile_pic" : obj.profile.profile_pic.url if obj.profile.profile_pic else "프로필 사진이 없습니다."}
    class Meta:
        model = Post
        fields = "__all__"

'''
이미지 호스팅 방법 알아보기,
노션에...
    데이터 형식 관련 키와 값에 대해서 설명
    값에 대한 데이터 타입 설명 필요
프로필 사진이 없다면 기본 이미지 url이 반환되도록
'''