from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as user_models


@admin.register(user_models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin Definition """

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {
            'fields': (
                "avatar",
                "gender",
                "bio",
                "birthdate",
                "language",
                "currency",
                "superhost",                
            ),
        }),
    )

    list_display = (
        "username",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
        "superhost",
    )

    list_filter = (
        "superhost",
        "gender",
        "language",
        "currency",
        "is_superuser",
        "is_staff",
    )
