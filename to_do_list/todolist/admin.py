from django.contrib import admin
from .models import UserMan, Task, Category
# Register your models here.


admin.site.register(UserMan)
admin.site.register(Task)
admin.site.register(Category)