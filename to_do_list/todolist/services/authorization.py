import todolist.models as models


class Authorization:
    @staticmethod
    def check_password(user: models.UserMan):
        try:
            for man in models.User.objects.filter(username=user.username,
                                               email=user.email):
                if man.password == user.password:
                    return True
                else:
                    raise Exception("Неверный пароль")
        except Exception as e:
            raise e