from django.contrib import admin
from . import models as reservation_models


@admin.register(reservation_models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "guest",
        "check_in",
        "check_out",
        "in_progress",
        "is_finished",
    )

    list_filter = (
        "status",
    )
