from django.urls import path
from . import views


app_name = "lists"

urlpatterns = [
    path("favs/", views.FavsView.as_view(), name="favs"),
    path("toggle/<int:pk>/", views.room_toggle_view, name="toggle"),
]