from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserTestCase(APITestCase):
    """ Тестирование API для пользователя """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')
        # Получаем администратора (у админа 2 курс и 2 урок)
        self.user = User.objects.get(email='admin@example.com')
        # Создаем клиент API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        """ Тест получения пользователя по ID """

        response = self.client.get(f'/users/update/{self.user.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Test_admin')

    def test_post_user(self):
        """ Тест создания пользователя """

        data = {
            "email": "new_admin@example.com",
            "first_name": "new_Test_admin",
            "password": "new_test_admin",
        }
        response = self.client.post('/users/register/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['first_name'], 'new_Test_admin')

    def test_list_users(self):
        """ Тест получения списка всех пользователей """

        response = self.client.get('/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

    def test_update_user(self):
        """ Тест изменения пользователя """

        data = {
            "email": "old_admin@example.com",
            "first_name": "old_Test_admin",
            "password": "old_test_admin",
        }
        response = self.client.put('/users/update/2/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'old_Test_admin')

    def test_delete_user(self):
        """ Тест удаления пользователя """

        response = self.client.delete(f'/users/delete/{self.user.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
