from django.contrib.auth.hashers import make_password
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from ..models import UserMan, Task
from ..forms import AuthorizationForm
from ..views import MainPage, create_task, edit_task, delete_task, read_task, home_page
from django.utils import timezone

class TestMainPage(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserMan(username="testuser", password=make_password("test", salt="point"), email="test@example.com", is_active=True, date_joined=timezone.now())
        self.user.save()
        self.url = reverse("authorization")

    def test_post_redirect(self):
        data = {'username': 'testuser', 'password': 'test', "email": "test@example.com"}
        request = self.factory.post(self.url, data)
        response = MainPage.as_view()(request)
        self.assertEqual(response.status_code, 302)



class TestCreateTask(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserMan(username="testuser", password=make_password("test", salt="point"), email="test@example.com", is_active=True, date_joined=timezone.now())
        self.user.save()
        self.url = reverse('create_task', args=[self.user.id])
        self.hash = self.user.password[-16::]

    def test_post_valid_data_creates_task(self):
        data = {'title': 'New Task', 'description': 'Details', 'priority': 3, 'due_date': "2025-04-25T05:15"}
        request = self.factory.post(f'{self.url}?hash={self.hash}', data)
        response = create_task(request, self.user.id)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

class TestTaskOperations(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserMan(username="testuser", password=make_password("test", salt="point"), email="test@example.com", is_active=True, date_joined=timezone.now())
        self.user.save()
        self.task = Task(user=self.user, title="Test Task",
                                        description="omg",
                                        completed=False, created_at=timezone.now(),
                                        updated_at=timezone.now(), due_date="2024-07-15 14:30:45.123456+03:00",
                                        priority=3)
        self.task.save()
        self.edit_url = reverse('edit_task', args=[self.user.id, self.task.id])
        self.delete_url = reverse('delete_task', args=[self.user.id, self.task.id])
        self.hash = self.user.password[-16::]

    def test_edit_task_updates_object(self):
        data = {'title': 'Updated', 'description': 'Details', 'priority': 3, 'due_date': "2025-04-25T05:15"}
        request = self.factory.post(f'{self.edit_url}?hash={self.hash}', data)
        response = edit_task(request, self.user.id, self.task.id)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated')

    def test_delete_task_removes_object(self):
        request = self.factory.get(f'{self.delete_url}?hash={self.hash}')
        response = delete_task(request, self.user.id, self.task.id)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TestReadTask(TestCase):
    def setUp(self):
        self.user = UserMan(username="testuser", password=make_password("test", salt="point"), email="test@example.com", is_active=True, date_joined=timezone.now())
        self.user.save()
        self.task = Task(user=self.user, title="Test Task",
                         description="omg",
                         completed=False, created_at=timezone.now(),
                         updated_at=timezone.now(), due_date="2024-07-15 14:30:45.123456+03:00",
                         priority=3)
        self.task.save()
        self.url = reverse('read_task', args=[self.user.id, self.task.id])
        self.hash = self.user.password[-16::]

    def test_cache_used_properly(self):
        self.factory = RequestFactory()
        request = self.factory.get(f'{self.url}?hash={self.hash}')
        response = read_task(request, self.user.id, self.task.id)
        self.assertEqual(response.status_code, 200)


        with self.assertNumQueries(1):
            response = read_task(request, self.user.id, self.task.id)
            self.assertEqual(response.status_code, 200)