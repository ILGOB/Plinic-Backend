import os
from pathlib import Path

import environ
import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from .models import Profile
from .serializers import PublicProfilePageSerializer, PrivateProfileSerializer

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

KAKAO_CALLBACK_URI = env("KAKAO_CALLBACK_URI")
REST_API_KEY = env("KAKAO_REST_API_KEY")

SERVER_IP = "http://127.0.0.1:8000"

LOGIN_STRAT_URL = reverse_lazy("kakao_login_start")
LOGIN_FINISH_URL = reverse_lazy("kakao_login_finish")
LOGIN_CALLBACK_MANAGE_URL = reverse_lazy("kakao-callback")


class ProfilePageView(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = "nickname"

    def get_queryset(self):
        return Profile.objects.filter(nickname=self.kwargs["nickname"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_serializer_class(self):
        if self.request.user.profile == self.get_object():
            return PrivateProfileSerializer
        return PublicProfilePageSerializer


def kakao_login_view(request):
    """
    카카오 서버에 로그인 요청
    """
    redirect_response = HttpResponseRedirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )
    return redirect_response


def kakao_callback_view(request):
    """
    인가 코드로 카카오 인증 서버로 Access Token Request
    code = 인가 코드
    access_token = 카카오로부터 받아온 access_token 값
    """
    print("----------kakao callback view 호출----------")
    code = request.GET.get("code")
    token_response_from_kakao = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
    )
    token_value_from_kakao = token_response_from_kakao.json()
    error = token_value_from_kakao.get("error")
    if error:
        return error
    access_token = token_value_from_kakao.get("access_token")

    # Email Request
    # 위에서 받아온 access token 으로, 카카오 인증 서버에서 해당 유저의 이메일을 받아옴
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    kakao_account = profile_request.get("kakao_account")
    print(kakao_account)
    email = kakao_account.get("email")

    # 위에서 받아온 이메일로 서버 내 데이터베이스에서 유저를 찾고,
    # 해당 유저가 없다면 새로운 유저를 가입한 후 서비스 서버의 access_token, refresh_token 발급
    user = get_user_model().objects.filter(email=email)

    # 데이터베이스에 카카오에서 받아온 이메일을 정보로 가지고 있는 유저가 있다면 로그인, 아니면 회원가입
    if user:
        # SocialAccount 모델에서 해당 유저를 찾고, social_user 에는 해당 객체가 담김
        social_user_qs = SocialAccount.objects.filter(user=user)
        print(social_user_qs)
        if social_user_qs:
            social_user = social_user_qs.first()
        else:
            social_user = None

        if social_user is None:
            # social_user 에 None 이 담겼다면, 이메일은 데이터베이스에 존재하지만 카카오 유저가 아닌 경우이므로 에러 메시지 출력
            return JsonResponse(
                {"error": "이메일은 존재하지만, 카카오 유저가 아닙니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if social_user.provider != "kakao":
            # social_user 의 provider 가 kakao 가 아니라면, 에러 메시지 출력
            return JsonResponse(
                {"error": "소셜 로그인 타입이 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            f"{SERVER_IP}{LOGIN_FINISH_URL}",
            data=data,
        )

        if accept.status_code != 200:
            return JsonResponse({"error": "회원가입에 실패했습니다."}, status=accept.status_code)

        accept_json = accept.json()
        accept_json.pop("user", None)

        return JsonResponse(accept_json)

    # 기존에 가입된 유저가 없으면 새로 가입
    else:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{SERVER_IP}{LOGIN_FINISH_URL}", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return HttpResponse(accept)
        accept_json = accept.json()
        accept_json.pop("user", None)

        return JsonResponse(accept_json)


class KakaoLoginView(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
