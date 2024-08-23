from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from lms.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """ Пользователь """
    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя')

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = PhoneNumberField(verbose_name='Телефон', default='+7', **NULLABLE)
    country = CountryField(verbose_name='Страна', default='RU', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Фото', **NULLABLE)
    about_message = models.TextField(verbose_name='О себе', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    """ Платежи """

    objects = models.Manager()

    payment_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Дата платежа')
    course = models.ForeignKey(Course,
                               **NULLABLE,
                               on_delete=models.SET_NULL,
                               verbose_name='Курс',
                               related_name='payment')
    lesson = models.ForeignKey(Lesson,
                               **NULLABLE,
                               on_delete=models.SET_NULL,
                               verbose_name='Урок',
                               related_name='payment')
    session_id = models.CharField(max_length=255,
                                  **NULLABLE,
                                  verbose_name='ID сессии',
                                  help_text='Укажите ID сессии')
    link = models.URLField(max_length=400,
                           **NULLABLE,
                           verbose_name='Ссылка на оплату',
                           help_text='Укажите ссылку на оплату')
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             **NULLABLE,
                             verbose_name='Пользователь',
                             help_text='Укажите пользователя',
                             related_name='payment')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user} - {self.course}'
