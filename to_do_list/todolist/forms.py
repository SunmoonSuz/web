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

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  # HTML5 datetime input
                    'class': 'form-control',  # CSS класс
                    'placeholder': 'YYYY-MM-DD HH:MM'
                }
            )
        }
