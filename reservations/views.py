import datetime
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from . import models as reservation_models
from rooms import models as room_models
from reviews import forms as review_forms


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        reservation_models.BookedDay.objects.get(date=date, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't reserve the room.")
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
        form = review_forms.CreateReviewForm()
        context = {
            "reservation": reservation,
            "form": form,
        }
        return render(self.request, "reservations/detail.html", context=context)


def reservation_update_view(request, pk, verb):
    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    if reservation is None or (
        reservation.guest != request.user
        and reservation.room.host != request.user
    ):
        raise Http404()

    if verb == "confirm":
        reservation.status = reservation_models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = reservation_models.Reservation.STATUS_CANCELED
        reservation_models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated.")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))

