import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedDay(core_models.DefaultModel):

    """ Check between days in Reservation item """

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    date = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="booked_days")

    def __str__(self):
        return f"{self.date} of {self.reservation.check_in} - {self.reservation.check_out}"


class Reservation(core_models.DefaultModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reservations")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return f"{self.room.name} - {self.check_in}"
    
    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            start = self.check_in
            end = self.check_out
            difference = end - start
            
            existing_booked_day = BookedDay.objects.filter(date__range=(start, end)).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    date = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(date=date, reservation=self)
                return
                    
        return super().save(*args, **kwargs)
