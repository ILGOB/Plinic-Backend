from rest_framework.routers import SimpleRouter
from django.urls import path, include
from . import views

post_router = SimpleRouter()
post_router.register("posts", views.PostViewSet)

notice_router = SimpleRouter()
notice_router.register("notices", views.NoticeViewSet)


urlpatterns = [
    path("", include(post_router.urls)),
    path("", include(notice_router.urls)),
    path("genres/", views.GenreListView.as_view()),
    path("random-thumbnail/", views.RandomThumbnailView.as_view()),
    path("random-playlist/", views.RandomPlayListView.as_view()),
    path("posts/<int:post_id>/likes/", views.LikeView.as_view()),
    path("playlists/<int:playlist_id>/scrappers/", views.ScrapView.as_view()),
    path("playlists/<str:nickname>/", views.PlaylistListView.as_view()),
    path(
        "random-background/",
        views.RandomBackgroundView.as_view(),
        name="random-background",
    ),
    path("get_dummy_data/", views.DummyDataView.as_view()),
    path("playlist-examples/", views.PlaylistExampleView.as_view()),
]
