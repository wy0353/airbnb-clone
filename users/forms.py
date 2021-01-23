from django import forms
from . import models as user_models


class LoginForm(forms.Form):

    """ Login Form Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = user_models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("The password is incorrect."))
        except user_models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("The user does not exist."))            


class JoinForm(forms.Form):

    """ Join Form Definition """

    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user_models.User.objects.get(username=email)
            return self.add_error("email", forms.ValidationError("The email already exist."))
        except user_models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            return self.add_error("password1", forms.ValidationError("The password does not match."))        
        return password

    def save(self):
        try:
            email = self.cleaned_data.get("email")
            first_name = self.cleaned_data.get("first_name")
            last_name = self.cleaned_data.get("last_name")
            password = self.cleaned_data.get("password")

            user = user_models.User.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return user
        except Exception as e:
            print(e)
            return None
