from email.policy import default

from django import forms
from django.core.exceptions import ValidationError
from.models import Task

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

class TaskForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(required=False)
    due_date = forms.DateTimeField(
        input_formats=['%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M'],
        widget=forms.TextInput(attrs={
            'class': 'datetime-input',
            'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'
        })
    )
    priority = forms.IntegerField()
