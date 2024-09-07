from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('videos/', get_videos,name="getvideos"),
]  
