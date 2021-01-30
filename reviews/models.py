from django.db import models
from core import models as core_models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(core_models.DefaultModel):

    """ Review Model Definition """

    class Meta:
        ordering = ("-created",)

    review = models.TextField()
    accuracy = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    cleanliness = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    location = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    check_in = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    value = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.review} in {self.room.name} ({self.user.username})"

    def rating_average(self):
        avg = (
            self.accuracy 
            + self.communication 
            + self.cleanliness 
            + self.location 
            + self.check_in 
            + self.value 
        ) / 6
        return round(avg, 2)
    rating_average.short_description = "Avg."
