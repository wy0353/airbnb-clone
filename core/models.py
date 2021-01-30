from django.db import models
from . import managers

class DefaultModel(models.Model):

    """ Default Model Definition """

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()
