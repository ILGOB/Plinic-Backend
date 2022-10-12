from .common import *

# INSTALLED_APPS += [
#     'debug_toolbar',
# ]

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third apps
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    # django-rest-auth
    'rest_framework_simplejwt.token_blacklist',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    # local apps
    'accounts.apps.AccountsConfig',
    'plinic',
    'debug_toolbar',
]

MIDDLEWARE = [
                 'debug_toolbar.middleware.DebugToolbarMiddleware',
             ] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1"]
