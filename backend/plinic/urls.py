from django.urls import path, include
from . import views

urlpatterns = [

    path('random-playlist', views.random_playlist_view.as_view()) 

]