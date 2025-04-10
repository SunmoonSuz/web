
import todolist.models as mo
from django.contrib.auth import get_user_model
from dataclasses import dataclass


@dataclass
class Userdef:
    username: str
    email: str
    password: str
    is_active: bool


class RegistrationUserInDb:
    @staticmethod
    def create_user(user: Userdef):
        mo.User(username = user.username, email=user.email,
                password=user.password, is_active=user.is_active).save()
