from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from . import views

router = SimpleRouter()
router.register("posts", views.PostViewSet)

urlpatterns = [

    #cr - get/post
    path('playlist/', views.random_play_list_create),
    #rud - get/put/delete
    #detail 미구현, get요청처리 작성필요
    path('playlist/<int:id>/', views.play_list_detail),

    path("", include(router.urls)),
]
