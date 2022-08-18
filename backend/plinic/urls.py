from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register("posts", views.PostViewSet)


urlpatterns = [

    path('random-playlist', views.random_playlist_view.as_view()),
    path("api/", include(router.urls)),
]
