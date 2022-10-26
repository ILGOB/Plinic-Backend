from django.urls import path
from . import views

urlpatterns = [
    path("kakao-auth/login/", views.kakao_login_view, name="kakao_login_start"),
    path(
        "kakao-authentication/callback/",
        views.kakao_callback_view,
        name="kakao_callback",
    ),
    path(
        "kakao-authentication/login/finish/",
        views.KakaoLoginView.as_view(),
        name="kakao_login_finish",
    ),
    path(
        "profiles/<str:nickname>/",
        views.ProfilePageView.as_view(),
    ),
]
