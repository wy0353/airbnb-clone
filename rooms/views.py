from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models as room_models


class HomeView(ListView):

    """ Home View Definition """

    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"


class RoomDetailView(DetailView):

    """ Room Detail View Definition """

    model = room_models.Room
