from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import forms
from rooms import models as room_models


def review_create_view(request, room):
    if request.method == "POST":
        form = forms.ReviewCreateForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if room is None:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room Review Created.")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
