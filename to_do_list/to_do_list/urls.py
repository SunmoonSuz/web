
from django.contrib import admin

import debug_toolbar
from django.urls import path, include
from django.urls import path, include
from todolist import views
import debug_toolbar
from django.urls import path
from todolist import views
import sys

sys.path.append("..")

urlpatterns = [
    path('authorization/', views.MainPage.as_view(), name="authorization"),
    path('register/', views.RegistrationPage.as_view(), name="register"),
    path('tasks/<int:user_id>/', views.home_page, name="home_page"),
    path('tasks/<int:user_id>/create/', views.create_task, name="create_task"),
    path('tasks/<int:user_id>/edit/<int:task_id>/', views.edit_task, name="edit_task"),
    path('tasks/<int:user_id>/delete/<int:task_id>/', views.delete_task, name="delete_task"),
    path('tasks/<int:user_id>/read/<int:task_id>/', views.read_task, name="read_task"),
    path('tasks/test/<int:user_id>/', views.test_task_list, name="test_list"),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
]
