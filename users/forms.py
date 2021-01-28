from django import forms
from . import models as user_models


class LoginForm(forms.Form):

    """ Login Form Definition """

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

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


class JoinForm(forms.ModelForm):

    """ Join Form Definition """

    class Meta:
        model = user_models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}), label="Confirm Password")

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

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            return self.add_error("password1", forms.ValidationError("The password does not match."))        
        return password

    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False)
        user.username = email
        user.set_password(password)
        user.save()
        return user
