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


class Genre(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Playlist(TimeStampedModel):
    title = models.CharField(max_length=150)
    url = models.URLField()
    thumbnail = models.ImageField(blank=True)
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, related_name="playlist_profile_set")
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    scrapper_set = models.ManyToManyField("accounts.Profile", related_name="playlist_scrapper_set")

    def __str__(self):
        return f'{self.pk}:{self.title}'


class Post(TimeStampedModel):
    profile = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=300)
    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE)
    voter_set = models.ManyToManyField("accounts.Profile", related_name="voter_set")
    tag_set = models.ManyToManyField("Tag", blank=True)

    def __str__(self):
        return f'{self.pk}:{self.title}'


class Tag(TimeStampedModel):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Notice(TimeStampedModel):
    author = models.ForeignKey("accounts.Profile", on_delete=models.DO_NOTHING)  # 관리자가 탈퇴해도 게시물은 지워지지 않도록 함
    title = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return f'{self.pk}:{self.title}'
