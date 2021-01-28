from django.urls import path
from . import views


app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.RoomUpdateView.as_view(), name="update"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/create/", views.PhotoCreateView.as_view(), name="create-photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
    path("<int:room_pk>/photos/<int:photo_pk>/update/", views.PhotoUpdateView.as_view(), name="update-photo"),
    path("search/", views.SearchView.as_view(), name="search"),
]