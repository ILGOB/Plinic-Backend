from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = SimpleRouter()
router.register("profiles", views.ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]