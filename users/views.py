from django.views import View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from . import forms as user_forms
from . import models as user_models


class UserJoinView(FormView):

    """ User Join View Definition """

    template_name = "users/join.html"
    form_class = user_forms.JoinForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Two",
        "last_name": "Tester",
        "email": "wy0353@gmail.com",
    }

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


class UserLoginView(FormView):

    """ User Login View Definition """

    template_name = "users/login.html"
    form_class = user_forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.email = email
            user.save()
        return super().form_valid(form)


class UserLogoutView(LogoutView):

    """ User Logout View Definition """

    next_page = reverse_lazy("core:home")


def complete_verification(request, key):
    print(key)
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = None
        user.save()
        # to do: add success message
    except user_models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))

