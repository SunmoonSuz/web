from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Model
from ..models import UserMan, Task
from ..forms import TaskForm, RegistrationForm
from django.core.cache import cache
import os
from django.core.serializers import serialize
import json

def take_object(type_object: Model, user_id: int, task_id: int | None) -> Task | UserMan:
    if type_object == UserMan:
        custom_object = type_object.objects.get(id=user_id)
        return custom_object
    elif type_object == Task:
        cache_key = str(task_id)
        custom_object = cache.get(cache_key)
        if not custom_object:
            current_user = UserMan.objects.get(id=user_id)
            custom_object = type_object.objects.get(user=current_user, id=task_id)
            cache.set(cache_key, custom_object, timeout=60)
        return custom_object
    else:
        raise ValueError("Model not found")




class TaskOperation:

    @staticmethod
    def create_task(form: TaskForm, user: UserMan) -> None:
        if not form.is_valid():
            raise ValidationError("Form is not valid")
        try:
            curr_task = Task(
                user=user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                completed=False,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                due_date=form.cleaned_data['due_date'],
                category=form.cleaned_data['category'],
                priority=form.cleaned_data['priority']
            )
            curr_task.save()
        except Exception as e:
            raise e
        cache.delete("task_list")



    @staticmethod
    def edit_task(form: TaskForm, task: Task, task_id: int) -> None:
        if not form.is_valid():
            raise ValidationError("Form is not valid")
        form.save()
        task.due_date = timezone.now()
        task.save()
        cache.delete(str(task_id))
        cache.delete("task_list")


class UserOperation:
    @staticmethod
    def create_user(form: RegistrationForm) -> None:
        if not form.is_valid():
            raise ValidationError("Form is not valid")
        try:
            UserMan(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password'], salt="point"),
                is_active=True, date_joined=timezone.now()
            ).save()
        except IntegrityError:
            raise IntegrityError("User is now defined")
        except Exception as e:
            raise e

def test_task_list(curr_user: UserMan) -> dict[str, dict]:
    query = '''SELECT id, category, due_date 
                            FROM todolist_task 
                            WHERE user_id = %s
                            GROUP BY id, category, due_date'''
    params = [curr_user.id]
    tasks = Task.objects.raw(query, params)
    task_list = dict()

    for task in tasks:
        due_date = task.due_date
        due_date = due_date.strftime("%Y-%m-%d")
        category = task.category

        if due_date not in task_list:
            task_list[due_date] = dict()

        if category not in task_list[due_date]:
            query = '''SELECT * 
            FROM todolist_task 
            WHERE user_id = %s
            AND DATE(due_date) = %s
            AND category = %s '''
            params = [curr_user.id, due_date, category]
            tasks_for_category = Task.objects.raw(query, params)

            task_list[due_date][category] = [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat(),
                'category': task.category
            } for task in tasks_for_category]

    return task_list