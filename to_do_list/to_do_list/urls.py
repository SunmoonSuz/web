"""
URL configuration for to_do_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todolist import views
import debug_toolbar
import sys

sys.path.append("..")

urlpatterns = [
    path('authorization/', views.MainPage.as_view(), name="authorization"),
    path('register/', views.RegistrationPage.as_view(), name="register"),
    path('tasks/<int:user_id>/', views.home_page),
    path('tasks/<int:user_id>/create/', views.create_task),
    path('tasks/<int:user_id>/edit/<int:task_id>/', views.edit_task),
    path('tasks/<int:user_id>/delete/<int:task_id>/', views.delete_task),
    path('tasks/<int:user_id>/read/<int:task_id>/', views.read_task),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls))
]
