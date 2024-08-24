from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson
from users.models import User


class UrlTestCase(APITestCase):
    """ Тестирование валидатора ссылок """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')
        # Получаем администратора (у админа 2 курс и 2 урок)
        self.user = User.objects.get(email='admin@example.com')
        # Создаем клиент API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Получаем курс
        self.course = Course.objects.get(title='Test Course2')

    def test_valid_lesson_video_url(self):
        """ Тестирование создания валидной ссылки на видео урока """

        data = {
            'course': self.course.pk,
            'title': 'Test lesson',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'owner': self.user.pk,
        }

        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertURLEqual(url1=response.json()['video_url'], url2='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.assertContains(response, 'www.youtube.com', status_code=201)


class CourseAPITestCase(APITestCase):
    """ Тестирование API для курсов """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')
        # Получаем администратора (у админа 2 курс и 2 урок)
        self.user = User.objects.get(email='admin@example.com')
        # Создаем клиент API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Получаем курс
        self.course = Course.objects.get(title='Test Course2')

    def test_get_course(self):
        """ Тест получения курса по ID """

        response = self.client.get(f'/courses/{self.course.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.course.title)

    def test_post_course(self):
        """ Тест создания курса """

        data = {
            'title': 'Test Course4',
            'description': 'Test description4'
        }
        response = self.client.post('/courses/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'Test Course4')

    def test_list_courses(self):
        """ Тест получения списка всех курсов """

        response = self.client.get('/courses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 3)

    def test_update_course(self):
        """ Тест изменения курса """

        data = {
            'title': 'Test Course2 Updated',
            'description': 'Test description2 Updated'
        }
        response = self.client.put(f'/courses/{self.course.pk}/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Test Course2 Updated')

    def test_delete_course(self):
        """ Тест удаления курса """

        response = self.client.delete(f'/courses/{self.course.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonAPITestCase(APITestCase):
    """ Тестирование API для уроков """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')
        # Получаем администратора (у админа 2 курс и 2 урок)
        self.user = User.objects.get(email='admin@example.com')
        # Создаем клиент API
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Получаем курс и урок
        self.course = Course.objects.get(title='Test Course2')
        self.lesson = Lesson.objects.get(course=self.course.pk)

    def test_get_lesson(self):
        """ Тест получения урока по ID """

        response = self.client.get(f'/lesson/{self.lesson.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], self.lesson.title)

    def test_post_lesson(self):
        """ Тест создания урока """

        data = {
            'title': 'Test_Lesson4',
            'description': 'Test description4',
            "video_url": "https://www.youtube.com/watch?v",
            "course": self.course.pk
        }
        response = self.client.post('/lesson/create/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['title'], 'Test_Lesson4')
        self.assertURLEqual(url1=response.json()['video_url'], url2='https://www.youtube.com/watch?v=')

    def test_list_lesson(self):
        """ Тест получения списка всех уроков """

        response = self.client.get('/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_update_lesson(self):
        """ Тест изменения урока """

        data = {
            'title': 'Test Lesson2 Updated',
            'description': 'Test description2 Updated',
            'course': self.course.pk
        }
        response = self.client.put(f'/lesson/update/{self.lesson.pk}/', data=data, format='json')
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Test Lesson2 Updated')

    def test_delete_lesson(self):
        """ Тест удаления урока """

        response = self.client.delete(f'/lesson/delete/{self.lesson.pk}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionAPITestCase(APITestCase):
    """ Тестирование API для подписки """

    def setUp(self) -> None:
        """ Создает экземпляры объектов для тестов """
        call_command('loaddata', 'test_data.json')

        # Получаем администратора (у админа 2 курс и 2 урок)
        self.user = User.objects.get(email='admin@example.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Получаем курс
        self.course = Course.objects.get(title='Test Course2')

    def test_post_subscribe(self):
        """ Тест создания подписки """

        data = {
            "course_id": self.course.id
        }

        response = self.client.post('/subscriptions/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscribe(self):
        """ Тест удаления подписки """
        data = {
            "course_id": self.course.id
        }

        response = self.client.post('/subscriptions/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
