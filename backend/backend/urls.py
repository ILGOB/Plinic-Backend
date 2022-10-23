from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Plinic API Document (for dev)",
        default_version="v1",
        description="플리닉 서비스 개발용 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/plinic/", include("plinic.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    # dj_rest_auth : 로그인 관련
    path("api/v1/accounts/", include("dj_rest_auth.urls")),
    # allauth : 소셜 로그인 관련
    path("api/v1/accounts/", include("allauth.urls")),
    # swagger
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
