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
