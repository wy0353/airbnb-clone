from django.contrib import admin
from . import models as review_models


@admin.register(review_models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    pass