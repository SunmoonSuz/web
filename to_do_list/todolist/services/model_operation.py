from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Model
from ..models import UserMan, Task
from ..forms import TaskForm, RegistrationForm
from django.core.cache import cache

def take_object(type_object: Model, user_id: int, task_id: int | None):
    try:
        if type_object == UserMan:
            object = type_object.objects.get(id=user_id)
        elif type_object == Task:
            task = cache.get(f"task{task_id}")
            if not task:
                current_user = UserMan.objects.get(id=user_id)
                object = type_object.objects.get(user=current_user, id=task_id)
                cache.set(f"task{task_id}", task, timeout=60)
        else:
            raise ValueError("Model isn't find")
    except type_object.DoesNotExist:
        raise type_object.DoesNotExist
    return object

class TaskOperation:

    @staticmethod
    def create_task(form: TaskForm, user: UserMan):
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
                priority=form.cleaned_data['priority']
            )
            curr_task.save()
        except Exception as e:
            raise e
        cache.delete("task_list")



    @staticmethod
    def edit_task(form: TaskForm, task: Task, task_id: int):
        if not form.is_valid():
            raise ValidationError("Form is not valid")
        form.save()
        task.due_date = timezone.now()
        task.save()
        cache.delete(f"task{task_id}")
        cache.delete("task_list")


class UserOperation:
    @staticmethod
    def create_user(form: RegistrationForm):
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