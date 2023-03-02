from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import TaskSerializer
from .models import Task
from datetime import datetime
import pytz


class AuthorizationTests(APITestCase):
    def setUp(self):
        # Создание юзеров
        self.user_test1 = User.objects.create_user(
            username="test1", email="test1@mail.ru", password="lq2w3e"
        )
        self.user_test1.save()

        # Создание токенов
        self.user_test1_token = Token.objects.create(user=self.user_test1)

        # Создание задачи
        self.test_task = Task.objects.create(
            header="test header",
            text="test text",
            date_of_completion=datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
            user=self.user_test1,
        )

        self.test_task.save()

    # Тестирование на защищенность API токеном всех API
    # Тестирование получения задач
    def test_invalid_tasks_view(self):
        response = self.client.get(reverse("tasks"), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_task_view(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("tasks"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование получения конкретной задачи
    def test_invalid_certain_tasks(self):
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.test_task.pk}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_certain_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.test_task.pk}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование создания задач
    def test_invalid_create_task(self):
        data = {
            "header": "test header",
            "text": "test text",
            "date_of_completion": datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
        }
        response = self.client.post(reverse("create-tasks"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        data = {
            "header": "test header",
            "text": "test text",
            "date_of_completion": datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
        }
        response = self.client.post(reverse("create-tasks"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Тестирование пометки задачи как выполненной
    def test_invalid_mark_completed_task(self):
        response = self.client.patch(
            reverse("mark-completed", kwargs={"pk": self.test_task.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_mark_completed(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.patch(
            reverse("mark-completed", kwargs={"pk": self.test_task.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Тестирование удаления задачи
    def test_invalid_delete_task(self):
        response = self.client.delete(
            reverse("delete-task", kwargs={"pk": self.test_task.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_valid_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.delete(
            reverse("delete-task", kwargs={"pk": self.test_task.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TaskTests(APITestCase):
    def setUp(self):
        # Создание юзеров
        user_test1 = User.objects.create_user(
            username="test1", email="test1@mail.ru", password="lq2w3e"
        )

        user_test2 = User.objects.create_user(
            username="test2", email="test2@mail.ru", password="lq2w4e"
        )

        # Создание токенов
        self.user_test1_token = Token.objects.create(user=user_test1)
        self.user_test2_token = Token.objects.create(user=user_test2)

        # Создание задач
        self.task_user1 = Task.objects.create(
            header="test header1",
            text="test text",
            date_of_completion=datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
            user=user_test1,
        )
        self.task_user2 = Task.objects.create(
            header="test header2",
            text="test text",
            date_of_completion=datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
            user=user_test2,
        )
        self.task_user1.save()
        self.task_user2.save()

    # Тестирование создания задачи
    def test_invalid_data_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        data = {
            "header": [123],
            "text": "test text",
            "date_of_completion": datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
        }
        response = self.client.post(reverse("create-tasks"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "header": "test header",
            "text": {"say": "hello"},
            "date_of_completion": datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
        }
        response = self.client.post(reverse("create-tasks"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "header": "test header",
            "text": {"test text"},
            "date_of_completion": "asd",
        }
        response = self.client.post(reverse("create-tasks"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_data_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        data = {
            "header": "test header",
            "text": "test text",
            "date_of_completion": datetime(
                2054, 10, 9, 23, 55, 59, 342380, tzinfo=pytz.UTC
            ),
        }
        post_response = self.client.post(
            reverse("create-tasks"), data=data, format="json"
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что действительно задача создана, и она выдается только конкретному юзеру
        serializer_result = TaskSerializer(post_response.data).data
        get_response = self.client.get(reverse("tasks"), format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_result, get_response.data)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test2_token.key)
        get_response = self.client.get(reverse("tasks"), format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_result, get_response.data)

    def test_get_tasks_for_current_user(self):
        # Тестируем для первого юзера
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(reverse("tasks"), format="json")
        serializer_task_user1 = TaskSerializer(self.task_user1).data
        serializer_task_user2 = TaskSerializer(self.task_user2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_task_user1, response.data)
        self.assertNotIn(serializer_task_user2, response.data)

        # Тестируем для второго юзера
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test2_token.key)
        response = self.client.get(reverse("tasks"), format="json")
        serializer_task_user1 = TaskSerializer(self.task_user1).data
        serializer_task_user2 = TaskSerializer(self.task_user2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_task_user2, response.data)
        self.assertNotIn(serializer_task_user1, response.data)

    def test_get_certain_task(self):
        # Первый юзер пытается получить совю задачу
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.task_user1.pk}), format="json"
        )
        serializer_task_user1 = TaskSerializer(self.task_user1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_task_user1, response.data)

        # Второй юзер пытается получить не совю задачу
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test2_token.key)
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.task_user1.pk}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Пытаемся получить несуществующую задачу
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)
        response = self.client.get(
            reverse(
                "certain-tasks", kwargs={"pk": self.task_user1.pk + self.task_user2.pk}
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_completed_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)

        # Проверяем, что задача не завершена
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.task_user1.pk}), format="json"
        )
        self.assertEqual(response.data.get("is_completed"), False)

        # Первый юзер пробует завершить свою задачу
        response = self.client.patch(
            reverse("mark-completed", kwargs={"pk": self.task_user1.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.task_user1.pk}), format="json"
        )
        # Проверяем, что задача выполнена
        self.assertEqual(response.data.get("is_completed"), True)

        # Первый юзер пробует завершить не свою задачу
        response = self.client.patch(
            reverse("mark-completed", kwargs={"pk": self.task_user2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_certain_task(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user_test1_token.key)

        # Первый юзер пытается удалить свою задачу
        response = self.client.delete(
            reverse("delete-task", kwargs={"pk": self.task_user1.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что задача действительно удалилась
        response = self.client.get(
            reverse("certain-tasks", kwargs={"pk": self.task_user1.pk}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Первый юзер пытается удалить не свою задачу
        response = self.client.delete(
            reverse("delete-task", kwargs={"pk": self.task_user2.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
