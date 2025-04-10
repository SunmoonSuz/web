import todolist.models as models


class Authorization:
    @staticmethod
    def check_password(user: models.UserMan, password: str):
        try:
            print(password, user.password)
            if password == user.password:
                return True
            else:
                raise Exception("Неверный пароль")
        except Exception as e:
            raise e