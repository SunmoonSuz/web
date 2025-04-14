from django.test import TestCase
from ..services.model_operation import take_object
from ..models import UserMan
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.cache import cache

class TestIntegration(TestCase):
    def test_service_flow(self):
        # 1. Работа с БД
        user = UserMan(username="testuser", password=make_password("test", salt="point"), email="test@example.com",
                       is_active=True, date_joined=timezone.now())
        user.save()

        # 2. Запись в Redis
        cache.set(f"user_{user.id}", "active", timeout=60)

        # 3. Проверка интеграции
        result = take_object(UserMan, user.id, None)
        assert result.username == "testuser"