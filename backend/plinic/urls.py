
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
router = SimpleRouter()

urlpatterns = [
    path('playlist/', views.random_play_list_create),
    path('playlist/<int:id>/', views.play_list_detail),
    path("", include(router.urls)),
]
