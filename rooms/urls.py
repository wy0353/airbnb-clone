from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.RoomUpdateView.as_view(), name="update"),
    path("search/", views.SearchView.as_view(), name="search"),
]