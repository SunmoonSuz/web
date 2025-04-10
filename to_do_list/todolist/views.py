
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import AuthorizationForm, RegistrationForm
from django.contrib import messages
from.models import UserMan
from.services import authorization
from django.utils.decorators import method_decorator
from django.utils import timezone
# Create your views here.


class MainPage(View):
    def get(self, request):
        auth_form = AuthorizationForm()
        return render(request, "main_page.html", {"form": auth_form})

    def post(self, request):
        auth_form = AuthorizationForm(request.POST)
        if not auth_form.is_valid():
            messages.error(request, "Исправьте ошибки в форме")
            return render(request, "main_page.html", {"form": auth_form})
        try:
            user = UserMan.objects.get(username=auth_form.cleaned_data['username'],
                                    email=auth_form.cleaned_data['email'])
            if authorization.Authorization.check_password(user):
                messages.success(request, "Вход прошёл успешно")
                return redirect('/login')
        except Exception as e:
            messages.error(request, f"Ошибка авторизации: {str(e)}")


class RegistrationPage(View):
    def get(self, request):
        reg_form = RegistrationForm()

        return render(request, "registration_page.html", {"form": reg_form})
    @method_decorator(csrf_protect)
    def post(self, request):
        reg_form = RegistrationForm(request.POST)
        if not reg_form.is_valid():
            messages.error(request, "Исправьте ошибки в форме")
            return render(request, "registration_page.html", {"form": reg_form})
        try:
            UserMan(
                username=reg_form.cleaned_data['username'],
                email=reg_form.cleaned_data['email'],
                password=make_password(reg_form.cleaned_data['password']),
                is_active=True, date_joined=timezone.now()

            ).save()
            response = redirect('/authorization')
            response.set_cookie('new_user', 'true', max_age=86400)
            messages.success(request, "Регистрация прошла успешно!")
            return response
        except IntegrityError:
            messages.error(request, "Пользователь с таким именем или email уже существует")
            return render(request, "registration_page.html", {"form": reg_form})
        except Exception as e:
            messages.error(request, f"Ошибка регистрации:  {str(e)}")
            return redirect('register')


def home_page(request):
    return HttpResponse()


def create_task(request):
    return HttpResponse()

def edit_task(request):
    return HttpResponse()

def read_task(request):
    return HttpResponse()