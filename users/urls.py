from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", register, name="register"),
    # path("add-profile/",add_profile,name="profileadd"),
    # path("profile/",profile,name="profile")
]  
