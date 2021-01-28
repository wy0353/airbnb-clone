import os
import requests
from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from . import mixins as user_mixins
from . import forms as user_forms
from . import models as user_models


class UserJoinView(user_mixins.LoggedOutOnlyView, FormView):

    """ User Join View Definition """

    template_name = "users/join.html"
    form_class = user_forms.JoinForm
    success_url = reverse_lazy("core:home")
    initial = {
        # "first_name": "Two",
        # "last_name": "Tester",
        # "email": "wy0353@gmail.com",
    }

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome {user.first_name}")
        user.verify_email()
        return super().form_valid(form)


class UserLoginView(user_mixins.LoggedOutOnlyView, FormView):

    """ User Login View Definition """

    template_name = "users/login.html"
    form_class = user_forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Hello {user.first_name}")
            user.email = email
            user.save()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get("next", None)
        if next_url is not None:
            print(next_url)
            return next_url
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:home"))


# class UserLogoutView(LogoutView):

#     """ User Logout View Definition """

#     next_page = reverse_lazy("core:home")


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = None
        user.save()
        messages.error(request, "Account need verify. Please check your email.")
    except user_models.User.DoesNotExist:
        messages.error(request, "User does not exist.")
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_url = "http://121.130.15.124:8003/users/login/github/callback/"
    scopes = "read:user"
    base_url = "https://github.com/"
    prefix = "login/oauth/authorize"
    query = f"?client_id={client_id}&redirect_url={redirect_url}&scope={scopes}"
    full_url = f"{base_url}{prefix}{query}"

    return redirect(full_url)


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)    
        if code is not None:
            client_id = os.environ.get("GITHUB_CLIENT_ID")
            client_secret = os.environ.get("GITHUB_CLIENT_SECRET")

            base_url = "https://github.com/"
            prefix = "login/oauth/access_token"
            query = f"?client_id={client_id}&client_secret={client_secret}&code={code}"
            full_url = f"{base_url}{prefix}{query}"
            res = requests.post(full_url, headers={
                "Accept": "application/json"
            })
            results = res.json()
            error = results.get("error", None)
            if error is not None:
                raise GithubException("Can't get authorization code.")
            else:
                access_token = results.get("access_token")
                user_results = requests.get("https://api.github.com/user", headers={
                    "Accept": "application/json",
                    "Authorization": f"token {access_token}",
                })
                github_user = user_results.json()
                username = github_user.get("login", None)
                if username is not None:
                    name = github_user.get("name")
                    email = github_user.get("email")
                    bio = github_user.get("bio")
                    try:
                        user = user_models.User.objects.get(email=email)
                        if user.login_method != user_models.User.LOGIN_GITHUB:
                            raise GithubException(f"Please Login with {user.login_method}")
                    except user_models.User.DoesNotExist:
                        user = user_models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=user_models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Hello {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get to your github profile.")
        else:
            raise GithubException("Can't get code.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_CLIENT_ID", None)
    if client_id is not None:
        redirect_uri = "http://121.130.15.124:8003/users/login/kakao/callback/"
        base_url = "https://kauth.kakao.com/"
        prefix = "oauth/authorize"
        query = f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        full_url = f"{base_url}{prefix}{query}"
        return redirect(full_url)
    
    return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            client_id = os.environ.get("KAKAO_CLIENT_ID", None)
            client_secret = os.environ.get("KAKAO_CLIENT_SECRET", None)
            redirect_uri = "http://121.130.15.124:8003/users/login/kakao/callback/"
            base_url = "https://kauth.kakao.com/"
            prefix = "oauth/token"
            query = f"?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}"
            full_url = f"{base_url}{prefix}{query}"
            res = requests.post(full_url, headers={
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            })
            results = res.json()
            error = results.get("error", None)
            if error is not None:
                raise KakaoException("Can't get authorization code.")
            access_token = results.get("access_token")

            base_url = "https://kapi.kakao.com/"
            prefix = "v2/user/me"
            full_url = f"{base_url}{prefix}"
            res = requests.get(full_url, headers={
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer {access_token}"
            })
            results = res.json()
            properties = results.get("properties")
            email = results["kakao_account"]["email"]
            if email is None:
                raise KakaoException("Please check the email is granted.")
            name = properties.get("nickname", None)
            profile_image = properties.get("profile_image", None)
            thumbnail_image = properties.get("thumbnail_image", None)
            try:
                user = user_models.User.objects.get(email=email)
                if user.login_method != user_models.User.LOGIN_KAKAO:
                    raise KakaoException(f"Please Login with {user.login_method}")

            except user_models.User.DoesNotExist:
                user = user_models.User.objects.create(
                    email=email,
                    first_name=name,
                    username=email,
                    login_method=user_models.User.LOGIN_KAKAO,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
                if profile_image is not None:
                    photo_res = requests.get(profile_image)                    
                    user.avatar.save(f"{name}-avatar.png", ContentFile(photo_res.content))
            login(request, user)
            messages.success(request, f"Hello {user.first_name}")
            return redirect(reverse("core:home"))
        else:
            raise KakaoException()
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class ProfileReadView(user_mixins.LoggedInOnlyView, DetailView):

    """ User Profile View Definition """

    model = user_models.User
    context_object_name = "user_obj"


class ProfileUpdateView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    """ User Update View Definition """
    success_message = "Profile updated."

    model = user_models.User
    context_object_name = "user"
    template_name = "users/user_update.html"
    fields = (
        "first_name",
        "last_name",
        "bio",
        "gender",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        return form


class PasswordUpdateView(
    user_mixins.LoggedInOnlyView, 
    user_mixins.EmailLoginOnlyView, 
    SuccessMessageMixin, 
    PasswordChangeView
):

    """ Password Update View Definition """
    
    template_name = "users/user_update_password.html"
    success_message = "Password updated."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs={"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs={"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs={"placeholder": "Confirm new password"}
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))
