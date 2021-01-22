from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """ Custom User Model Definition """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_CHOICES = (
        (CURRENCY_KRW, "KRW"),
        (CURRENCY_USD, "USD"),
    )

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, default=GENDER_OTHER, max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True, default=None)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, default=LANGUAGE_KOREAN, max_length=2, null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES, default=CURRENCY_KRW, max_length=3, null=True, blank=True)
    superhost = models.BooleanField(default=False)

