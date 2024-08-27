from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from users.models import User


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


@shared_task
def deactivate_inactive_users():
    """
    Отключение неактивных пользователей.
    Если пользователь не заходил более месяца, блокировать его с помощью флага is_active
    """
    inactive_period = timezone.now() - timedelta(seconds=30)
    inactive_users = User.objects.filter(last_login__gt=inactive_period, is_active=True, is_superuser=False)

    for user in inactive_users:
        user.is_active = False
        user.save()

        print(f'Пользователь с email: {user.email} был заблокирован, ввиду отсутствия онлайн более 30 дней')

        send_mail(
            subject='Блокировка',
            message=f'Пользователь с email: {user.email} был деактивирован из-за отсутствия активности более 30 дней',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]

        )

    if inactive_users is not None:
        print("Пользователи были неактивны в течении 30 дней и был деактивированы.")
