from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    img = serializers.CharField(source='profile_pic')
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'img']
