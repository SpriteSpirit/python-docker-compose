from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from lms.models import Course
from lms.validators import UrlValidator
from users.models import User


class UrlTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_valid_lesson_video_url(self):
        """ Тестирование создания валидной ссылки на видео урока """

        test_user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            password='test',
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )

        Course.objects.create(
            title='Test Course',
            description='Test course description',
            owner=test_user
        )

        data = {
            'course': 1,
            'title': 'Test lesson',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'owner': 1
        }

        response = self.client.post('/lesson/create/', data=data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



        # with self.assertRaises(ValidationError) as e:
        #     UrlValidator(url=data['video_url'])
        # self.assertEqual(str(e.exception.detail), 'Invalid URL')
