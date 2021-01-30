import datetime
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from . import models as reservation_models
from rooms import models as room_models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        reservation_models.BookedDay.objects.get(date=date, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error("Can't reserve the room.")
        return redirect(reverse("core:home"))
    except reservation_models.BookedDay.DoesNotExist:
        reservation = reservation_models.Reservation.objects.create(
            check_in=date,
            check_out=date + datetime.timedelta(days=1),
            guest=request.user,
            room=room,
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):

    """ Reservation Detail View Definition """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
        if reservation is None or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()

        return render(self.request, "reservations/detail.html", {"reservation": reservation})
        

