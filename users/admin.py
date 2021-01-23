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
                "login_method",
                "email_verified",
                "email_secret",
            ),
        }),
    )

    list_display = (
        "username",
        "avatar",
        "gender",
        "birthdate",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = (
        "superhost",
        "gender",
        "language",
        "currency",
        "login_method",
        "is_superuser",
        "is_staff",
    )
