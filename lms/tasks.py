from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_course_update_email(user_email: str, course_name: str):
    """ Отправка сообщения пользователю при обновлении курса """
    send_mail(
        subject=f'Курс {course_name} обновлен',
        message=f'Вышло обновление курса {course_name}. Проверьте новые материалы!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )
    print(f'Отправлено письмо пользователю {user_email} об изменении в курсе {course_name}')


@shared_task
def send_lesson_update_email(user_email: str, course_name: str, lesson_name: str):
    """ Отправка сообщения пользователю при обновлении курса """
    send_mail(
        subject=f'Урок {lesson_name} курса {course_name} обновлен',
        message=f'Вышло обновление урока {lesson_name}\nКурс: {course_name}. Проверьте новые материалы!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )
    print(f'Отправлено письмо пользователю {user_email} об изменении в уроке {lesson_name} курса {course_name}')

