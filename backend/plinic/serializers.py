from rest_framework import serializers
from .models import Post
from accounts.serializers import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


'''
노션에...
    데이터 형식 관련 키와 값에 대해서 설명
    값에 대한 데이터 타입 설명 필요
프로필 사진이 없다면 기본 이미지 url이 반환되도록
디폴트 프로필 이미지는 로고로!
'''
