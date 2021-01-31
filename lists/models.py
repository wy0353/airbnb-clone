from django.db import models
from core import models as core_models


class List(core_models.DefaultModel):

    """ List Model Definition """

    name = models.CharField(max_length=80)
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="list")
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "Number of Rooms"
