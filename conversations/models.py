from django.db import models
from core import models as core_models


class Conversation(core_models.DefaultModel):

    """ Conversation Model Definition """

    participants = models.ManyToManyField("users.User", blank=True)\


    def __str__(self):
        return f"{self.created}"


class Message(core_models.DefaultModel):

    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE, related_name="messages")

    def __str__(self):
        return f"{self.user} : {self.message}"