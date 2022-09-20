from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('plinic-api/', include("plinic.urls")),
    path('accounts-api/', include("accounts.urls")),
    path('accounts-api/', include('dj_rest_auth.urls')),
    path('accounts-api/', include('allauth.urls')),
    path('accounts-api/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
