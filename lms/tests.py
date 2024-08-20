from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase


class UrlTestCase(APITestCase):
    """ Тестирование валидатора ссылок """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')

    def test_valid_lesson_video_url(self):
        """ Тестирование создания валидной ссылки на видео урока """

        data = {
            'course': 1,
            'title': 'Test lesson',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'owner': 1
        }

        response = self.client.post('/lesson/create/', data=data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertURLEqual(url1=response.json()['video_url'], url2='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertContains(response, 'www.youtube.com', status_code=201)


class CourseAPITestCase(APITestCase):
    """ Тестирование API для курсов """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')