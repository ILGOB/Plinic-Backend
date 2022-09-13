from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views

router = SimpleRouter()
router.register("posts", views.PostViewSet)

urlpatterns = [

    path('random-playlist', views.random_play_list_view),
    path('random-playlist/', views.random_play_list_create),
    path("", include(router.urls)),
]
