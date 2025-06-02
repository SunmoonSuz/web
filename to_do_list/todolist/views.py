from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.exceptions import ValidationError
from .forms import AuthorizationForm, RegistrationForm, TaskForm
from django.contrib import messages
from .models import UserMan, Task
from .services import authorization, model_operation, access
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import connection


# Create your views here.
def new_page(View):
    pass

class MainPage(View):
    @staticmethod
    def get(request):
        auth_form = AuthorizationForm()
        return render(request, "main_page.html", {"form": auth_form})

    @staticmethod
    def post(request):
        auth_form = AuthorizationForm(request.POST)
        try:
            user_id, password = authorization.Authorization.entrance(auth_form)
        except ValidationError as e:
            messages.error(request, f"Исправьте ошибки в форме: {str(e)}")
            return render(request, "main_page.html", {"form": auth_form})
        except Exception as e:
            messages.error(request, f"Ошибка авторизации: {str(e)}")
            return render(request, "main_page.html", {"form": auth_form})
        return redirect(f'/tasks/{user_id}?hash={password[-16::]}')

class RegistrationPage(View):
    @staticmethod
    def get(request):
        reg_form = RegistrationForm()
        return render(request, "registration_page.html", {"form": reg_form})

    @staticmethod
    def post(request):
        reg_form = RegistrationForm(request.POST)
        try:
           model_operation.UserOperation.create_user(reg_form)
        except IntegrityError:
            messages.error(request, "Пользователь с таким именем или email уже существует")
            return render(request, "registration_page.html", {"form": reg_form})
        except Exception as e:
            messages.error(request, f"Ошибка регистрации:  {str(e)}")
            return redirect('register')
        response = redirect('/authorization')
        response.set_cookie('new_user', 'true', max_age=86400)
        return response

def home_page(request, user_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError as e:
        return JsonResponse(str(e), status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    tasks = cache.get("task_list")
    if not tasks:
        current_user = model_operation.take_object(UserMan, user_id, None)
        tasks = Task.objects.filter(user=current_user)
        cache.set("task_list", tasks, timeout=60)
    page = request.GET.get("page")
    paginator = Paginator(tasks, 5)
    page_obj = paginator.get_page(page)
    return render(request, "login_page.html",
                  {"hash": user_hash, "id": user_id, "page_obj": page_obj})


def create_task(request, user_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError:
        return JsonResponse("Unauthorized access", status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    try:
        current_user = model_operation.take_object(UserMan, user_id, None)
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse(str(e), status=404)

    if request.method != "POST":
        task_form = TaskForm()
        return render(request, "create_task_page.html",
                      {"form": task_form, "hash": user_hash, "id": user_id})
    task_form = TaskForm(request.POST)
    try:
        model_operation.TaskOperation.create_task(task_form, current_user)
    except ValidationError as e:
        messages.error(request, f"Исправьте ошибки в форме: {str(e)}")
        return render(request, "edit_task_page.html", {"form": task_form, "id": user_id, "hash": user_hash})
    except Exception as e:
        messages.error(request, f"Ошибка при создании задачи: {str(e)}")
        return render(request, "create_task_page.html",
                      {"form": task_form, "hash": user_hash, "id": user_id})
    response = redirect(f'/tasks/{user_id}?hash={user_hash}')
    response.set_cookie('new_task', 'true', max_age=86400)

    return response



def edit_task(request, user_id, task_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError:
        return JsonResponse("Unauthorized access", status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    try:
        task = model_operation.take_object(Task, user_id, task_id)
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse(str(e), status=404)
    if request.method != "POST":
        task_form = TaskForm(instance=task)
        return render(request, "edit_task_page.html", {"form": task_form, "id": user_id, "hash": user_hash})
    task_form = TaskForm(request.POST, instance=task)
    try:
        model_operation.TaskOperation.edit_task(task_form, task, task_id)
    except ValidationError as e:
        messages.error(request, f"Исправьте ошибки в форме: {str(e)}")
        return render(request, "edit_task_page.html", {"form": task_form, "id": user_id, "hash": user_hash})

    return redirect(f"http://127.0.0.1:8000/tasks/{user_id}?hash={hash}")


def read_task(request, user_id, task_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError:
        return JsonResponse("Unauthorized access", status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    try:
        task = model_operation.take_object(Task, user_id, task_id)
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse(str(e), status=404)
    return render(request, "read_task_page.html",
                  {"task": task, "user_id": user_id, "hash": user_hash})

def delete_task(request, user_id, task_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError:
        return JsonResponse("Unauthorized access", status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    try:
        task = model_operation.take_object(Task, user_id, task_id)
    except Exception as e:
        messages.error(request, str(e))
        return JsonResponse(str(e), status=404)
    task.delete()
    cache.delete(str(task_id))
    cache.delete("task_list")
    return redirect(f"http://127.0.0.1:8000/tasks/{user_id}?hash={user_hash}")


def test_task_list(request, user_id):
    user_hash = request.GET.get("hash")
    try:
        access.access(user_hash, user_id)
    except ValueError as e:
        return JsonResponse(str(e), status=403)
    except Exception as e:
        return JsonResponse(str(e), status=404)
    current_user = model_operation.take_object(UserMan, user_id, None)
    tasks = model_operation.test_task_list(current_user)
    return JsonResponse(tasks)



