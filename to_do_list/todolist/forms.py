from django import forms
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают!")

        return cleaned_data

class AuthorizationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(min_length=3, max_length=10)
    password = forms.CharField(min_length=4)

