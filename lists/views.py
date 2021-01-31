from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from . import models as list_models
from rooms import models as room_models


def room_toggle_view(request, pk):
    action = request.GET.get("action", None)
    if action is not None:
        room = room_models.Room.objects.get_or_none(pk=pk)
        if room is not None:
            the_list, created = list_models.List.objects.get_or_create(
                user=request.user, name="My Favourite Houses"
            )
            if action == "add":
                the_list.rooms.add(room)
            elif action == "remove":
                the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": pk}))


class FavsView(TemplateView):

    """ Favs View Definition """

    template_name = "lists/favs.html"
