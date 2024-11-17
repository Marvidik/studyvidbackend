from django.contrib import admin
from django.urls import path,include,re_path
from .views import *
from .views import GoogleLogin,GoogleLoginCallback,GoogleLoginRedirect

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", register, name="register"),
    # path("add-profile/",add_profile,name="profileadd"),
    # path("profile/",profile,name="profile")
    
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    re_path(r"^api/v1/auth/accounts/", include("allauth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/google/login/", GoogleLoginRedirect.as_view(), name="google_login_redirect"),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("api/v1/auth/google/callback/", GoogleLoginCallback.as_view(), name="google_login_callback"),
]  
