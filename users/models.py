from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


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
