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
    """ Оплата """

    objects = models.Manager()

    PAYMENT_METHODS = (
        ('card', 'Карта'),
        ('cash', 'Наличные'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=10, verbose_name='Метод оплаты')