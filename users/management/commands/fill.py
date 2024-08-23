import json
from django.core.management import BaseCommand
from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = 'Заполнение базы данными из JSON-файлов'
    json_name = "data_base.json"

    @staticmethod
    def json_read_courses(json_file_name):
        courses = []

        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "lms.course":
                    courses.append(item)

        return courses

    @staticmethod
    def json_read_lessons(json_file_name):
        lessons = []

        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "lms.lesson":
                    lessons.append(item['fields'])

        return lessons

    @staticmethod
    def json_read_users(json_file_name):
        users = []

        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "users.user":
                    users.append(item)

        return users

    @staticmethod
    def json_read_payments(json_file_name):
        payments = []

        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "users.payment":
                    payments.append(item['fields'])

        return payments

    def handle(self, *args, **options):
        # Удаление всех объектов
        Payment.objects.all().delete()
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()

        # Заполнение базы данными из JSON-файлов
        courses_for_create = []
        lessons_for_create = []
        users_for_create = []
        payments_for_create = []

        # Создание курсов
        for course in Command.json_read_courses(self.json_name):
            courses_for_create.append(Course(pk=course['pk'],
                                             title=course['fields']['title'],
                                             preview=course['fields']['preview'],
                                             description=course['fields']['description']
                                             ))

        Course.objects.bulk_create(courses_for_create)

        # Создание уроков с привязкой к курсам
        for lesson in Command.json_read_lessons(self.json_name):
            course_pk = lesson.pop('course')
            course_instance = Course.objects.get(pk=course_pk)

            lessons_for_create.append(Lesson(course=course_instance, **lesson))

        Lesson.objects.bulk_create(lessons_for_create)

        # Создание пользователей
        for user in Command.json_read_users(self.json_name):
            users_for_create.append(User(pk=user['pk'],
                                         password=user['fields']['password'],
                                         is_superuser=user['fields']['is_superuser'],
                                         is_staff=user['fields']['is_staff'],
                                         is_active=user['fields']['is_active'],
                                         date_joined=user['fields']['date_joined'],
                                         first_name=user['fields']['first_name'],
                                         email=user['fields']['email'],
                                         phone=user['fields']['phone'],
                                         country=user['fields']['country'],
                                         avatar=user['fields']['avatar'],
                                         about_message=user['fields']['about_message'],
                                         ))
        User.objects.bulk_create(users_for_create)

        # Cоздание платежей с привязкой к пользователям, курсам и урокам
        for payment in Command.json_read_payments(self.json_name):
            user = User.objects.get(pk=payment.pop('user'))
            course = None
            lesson = None

            if payment['course']:
                course = Course.objects.get(pk=payment.pop('course'))
            if payment['lesson']:
                lesson = Lesson.objects.get(pk=payment.pop('lesson'))

            payments_for_create.append(Payment(
                user=user,
                course=course,
                lesson=lesson,
                payment_date=payment['payment_date'],
            ))
        Payment.objects.bulk_create(payments_for_create)
