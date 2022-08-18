from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views

router = SimpleRouter()
router.register("posts", views.PostViewSet)

urlpatterns = [

    path('random-playlist', views.random_playlist_view.as_view()),
    path("", include(router.urls)),
]
