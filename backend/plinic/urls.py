from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views

router = SimpleRouter()
router.register("posts", views.PostViewSet)
router.register("playlists", views.PlaylistViewSet)
router.register("notices", views.NoticeViewSet)

urlpatterns = [
    path('random-thumbnail/', views.RandomThumbnailView.as_view()),
    path('random-playlist/', views.RandomPlayListView.as_view()),
    path("", include(router.urls)),
]
