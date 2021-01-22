from django.db import models
from core import models as core_models


class Review(core_models.DefaultModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField(default=0)
    communication = models.IntegerField(default=0)
    cleanliness = models.IntegerField(default=0)
    location = models.IntegerField(default=0)
    check_in = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.review} in {self.room.name} ({self.user.username})"
