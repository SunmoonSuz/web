from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import AuthorizationForm, RegistrationForm, TaskForm
from django.contrib import messages
from.models import UserMan, Task, Category
from.services import authorization
from django.utils.decorators import method_decorator
from django.utils import timezone
<<<<<<< HEAD
from django.core.paginator import Paginator

=======
from rest_framework import viewsets
from .serializers import TaskSerializer
>>>>>>> 671a07a4004e36d1a83fcc188ca86a52831239ae
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
            user_id = user.id
            password = make_password(auth_form.cleaned_data['password'], salt="point")
            if authorization.Authorization.check_password(user, password):
                messages.success(request, "Вход прошёл успешно")
                return redirect(f'/tasks/{user_id}?hash={password[-16::]}')
        except Exception as e:
            messages.error(request, f"Ошибка авторизации: {str(e)}")
            return render(request, "main_page.html", {"form": auth_form})


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
                password=make_password(reg_form.cleaned_data['password'], salt="point"),
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



def home_page(request, user_id):
    hash = request.GET.get("hash")
<<<<<<< HEAD
    page = request.GET.get("page")

    current_user = UserMan.objects.get(id=user_id)
    tasks = Task.objects.filter(user=current_user)
    paginator = Paginator(tasks, 5)
    page_obj = paginator.get_page(page)
    return render(request, "login_page.html",
                  {"hash": hash, "id": user_id, "page_obj": page_obj})
=======
    current_user = UserMan.objects.get(id=user_id)
    tasks = Task.objects.filter(user=current_user)
    return render(request, "login_page.html", {"tasks": tasks, "hash": hash, "id": user_id})
>>>>>>> 671a07a4004e36d1a83fcc188ca86a52831239ae


def create_task(request, user_id):
    hash = request.GET.get("hash")

    try:
        current_user = UserMan.objects.get(id=user_id)
    except UserMan.DoesNotExist:
        messages.error(request, "Пользователь не найден")
        return JsonResponse('User does not exist', status=403)

    if request.method != "POST":
        task_form = TaskForm()
        return render(request, "create_task_page.html",
                      {"form": task_form, "hash": hash, "id": user_id})

    task_form = TaskForm(request.POST)
    if not task_form.is_valid():
        print(task_form)
        messages.error(request, "Исправьте ошибки в форме")
        return render(request, "create_task_page.html",
                      {"form": task_form, "hash": hash, "id": user_id})

    try:
        curr_task = Task(
            user=current_user,
            title=task_form.cleaned_data['title'],
            description=task_form.cleaned_data['description'],
            completed=False,
            created_at=timezone.now(),
            updated_at=timezone.now(),
            due_date=task_form.cleaned_data['due_date'],
            priority=task_form.cleaned_data['priority']
        )
        curr_task.save()

        response = redirect(f'/tasks/{user_id}?hash={hash}')
        response.set_cookie('new_task', 'true', max_age=86400)
        return response

    except Exception as e:
        messages.error(request, f"Ошибка при создании задачи: {str(e)}")
        return render(request, "create_task_page.html",
                      {"form": task_form, "hash": hash, "id": user_id})

def edit_task(request, user_id, task_id):
    hash = request.POST.get("hash")
    try:
        current_user = UserMan.objects.get(id=user_id)
    except UserMan.DoesNotExist:
        messages.error(request, "Пользователь не найден")
        return JsonResponse('User does not exist', status=403)

    task = Task.objects.get(user = current_user, id=task_id)
    if request.method != "POST":
        task_form = TaskForm(instance=task)
        return render(request, "edit_task_page.html", {"form": task_form, "id": user_id, "hash": hash})

    task_form = TaskForm(request.POST, instance=task)
    if not task_form.is_valid():
        messages.error(request, "Исправьте ошибки в форме")
        return render(request, "edit_task_page.html",
                      {"form": task_form, "hash": hash, "id": user_id})

    task_form.save()
    task.due_date = timezone.now()
    task.save()
<<<<<<< HEAD
    return redirect(f"http://127.0.0.1:8000/tasks/{user_id}?hash={hash}")

def read_task(request, user_id, task_id):
    hash = request.GET.get("hash")
    curr_user = UserMan.objects.get(id=user_id)
    task = Task.objects.get(user=curr_user, id=task_id)

    return render(request, "read_task_page.html",
                  {"task": task, "user_id": user_id, "hash": hash})

def delete_task(request, user_id, task_id):
    hash = request.GET.get("hash")
    try:
        curr_user = UserMan.objects.get(id=user_id)
    except UserMan.DoesNotExist:
        messages.error(request, "Пользователь не найден")
        return JsonResponse('User does not exist', status=403)
    Task.objects.filter(user=curr_user, id=task_id).delete()
    return redirect(f"http://127.0.0.1:8000/tasks/{user_id}?hash={hash}")
=======
    return redirect(f'http://127.0.0.1:8000/tasks/{user_id}?hash={hash}')

def read_task(request):
    return render()

def delete_task(request):
    return render()
>>>>>>> 671a07a4004e36d1a83fcc188ca86a52831239ae
