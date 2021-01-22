from django.contrib import admin
from . import models as reservation_models


@admin.register(reservation_models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    pass
