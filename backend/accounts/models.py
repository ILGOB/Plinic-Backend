from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    '''
    모든 모델의 기본이 되는 TimeStampedModel
    생성일자, 수정일자가 자동 추가되도록
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=150, unique=True, null=True)
    profile_pic = models.ImageField(null=True, upload_to="profiles/%Y/%m/%d")

    def __str__(self):
        return f'{self.pk}:{self.user.username} Profile'
