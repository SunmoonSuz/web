
from django.db import models


# Create your models here.
class UserMan(models.Model):
    username = models.CharField()
    email = models.EmailField()
    password = models.CharField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        db_table = 'todolist_userman'

class Task(models.Model):
    user = models.ForeignKey(UserMan, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    priority = models.IntegerField(default=0, choices=((i, i) for i in range(1, 6)))
    due_date = models.DateTimeField()
class Category(models.Model):
    user = models.ForeignKey(UserMan, on_delete=models.CASCADE)
    name = models.CharField()
    color = models.CharField(max_length=7)