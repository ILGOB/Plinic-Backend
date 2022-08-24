from django.contrib import admin

from .models import Genre, Post, Notice, Playlist, Tag, Track


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    pass


@admin.register(Playlist)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
