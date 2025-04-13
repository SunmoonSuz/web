import todolist.models as models
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from ..forms import AuthorizationForm
from ..models import UserMan


class Authorization:
    @staticmethod
    def check_password(user: models.UserMan, password: str):
        user_password = make_password(password, salt="point")
        try:
            if user_password == user.password:
                return True
            else:
                raise Exception("Неверный пароль")
        except Exception as e:
            raise e
    @staticmethod
    def entrance(form: AuthorizationForm):
        if not form.is_valid():
            raise ValidationError

        try:
            user = UserMan.objects.get(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'])
        except Exception as e:
            raise e
        user_id = user.id
        password = form.cleaned_data['password']
        if Authorization.check_password(user, password):
            password = make_password(password, salt='point')
            return user_id, password