from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = SimpleRouter()
router.register("profiles", views.ProfileViewSet)

urlpatterns = [
    # path("", include(router.urls)),
    path('kakao-authentication/login/', views.kakao_login),
    path('kakao-authentication/callback/', views.kakao_callback),
    path('kakao-authentication/login/finish/', views.KakaoLogin.as_view()),
]
