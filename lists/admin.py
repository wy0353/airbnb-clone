from django.contrib import admin
from . import models as list_models


@admin.register(list_models.List)
class ListAdmin(admin.ModelAdmin):

    """ List Admin Model Definition """

    pass
