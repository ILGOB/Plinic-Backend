from django.contrib import admin

from .models import Genre, Post, Notice, Playlist, Tag


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
