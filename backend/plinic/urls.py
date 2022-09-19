
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
router = SimpleRouter()

urlpatterns = [
    #cr - get/post
    path('playlist/', views.random_play_list_create),
    #rud - get/put/delete
    #detail 미구현, get요청처리 작성필요
    path('playlist/', views.random_play_list_create),
    path('playlist/<int:id>/', views.play_list_detail),
    path("", include(router.urls)),
]
