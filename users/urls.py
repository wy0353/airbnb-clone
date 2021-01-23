from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("join/", views.UserJoinView.as_view(), name="join"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
]