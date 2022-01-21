from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('youtubemusic', views.youtubemusic, name='youtubemusic'),
    path('spotify', views.spotify, name='spotify'),
]