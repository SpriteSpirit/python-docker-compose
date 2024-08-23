from django.db import models
from config import settings

# поле становится необязательным как на уровне базы данных, так и на уровне формы
NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """ Курс """
    objects = models.Manager()

    title = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='courses/preview/', verbose_name='Изображение', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses', **NULLABLE)
    price = models.PositiveIntegerField(default=10000, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """ Урок """
    objects = models.Manager()

    title = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    preview = models.ImageField(upload_to='lessons/preview/', verbose_name='Изображение', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons', **NULLABLE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """ Подписка """

    objects = models.Manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscription',
                             on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, related_name='subscription', on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} - {self.course}'
