import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import reverse


class User(AbstractUser):

    """ Custom User Model Definition """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "ko"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_KRW = "krw"
    CURRENCY_USD = "usd"
    CURRENCY_CHOICES = (
        (CURRENCY_KRW, "KRW"),
        (CURRENCY_USD, "USD"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    gender = models.CharField(_('gender'), choices=GENDER_CHOICES, default=GENDER_OTHER, max_length=10, null=True, blank=True)
    bio = models.TextField(_('bio'), null=True, blank=True, default=None)
    birthdate = models.DateField(_('birthdate'), null=True, blank=True)
    language = models.CharField(_('language'), choices=LANGUAGE_CHOICES, default=LANGUAGE_KOREAN, max_length=2, null=True, blank=True)
    currency = models.CharField(_('currency'), choices=CURRENCY_CHOICES, default=CURRENCY_KRW, max_length=3, null=True, blank=True)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default=None, null=True, blank=True)
    login_method = models.CharField(max_length=10, choices=LOGIN_CHOICES, null=True, blank=True, default=LOGIN_EMAIL)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        try:
            if self.email_verified is False:
                secret_key = uuid.uuid4().hex[:20]
                self.email_secret = secret_key
                html_message = render_to_string("emails/verify_email.html", {"secret_key": secret_key})
                send_mail(
                    _("Verify Earbnb Account"),
                    strip_tags(html_message),
                    settings.EMAIL_FROM,
                    [self.email],
                    fail_silently=False,
                    html_message=html_message
                )
                self.save()
        except Exception as e:
            print(e)
