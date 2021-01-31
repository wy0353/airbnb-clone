from django.urls import path
from rooms import views as room_views
from . import views as core_views


app_name = "core"

urlpatterns = [
    path("language-switch/", core_views.language_switch_view, name="language-switch"),
    path("", room_views.HomeView.as_view(), name="home"),
]