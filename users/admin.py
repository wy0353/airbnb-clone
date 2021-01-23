from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from helpers.django.admin.utils import url_to_html_img
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
        "get_avatar",
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

    def get_avatar(self, obj):
        if bool(obj.avatar):
            return url_to_html_img(obj.avatar.url)
        else:
            return None
    get_avatar.short_description = "avatar"
