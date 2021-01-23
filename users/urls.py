from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("join/", views.UserJoinView.as_view(), name="join"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("verify/<str:key>/", views.complete_verification, name="complete_verification"),
]