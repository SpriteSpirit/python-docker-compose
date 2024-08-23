from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор урока """

    video_url = serializers.CharField(required=False, validators=[UrlValidator('video_url')])

    class Meta:
        model = Lesson
        fields = '__all__'
        # validators = [UrlValidator(url='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор курса """

    # Добавляем поле с числом уроков в курсе
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        """ Проверяем подписку текущего пользователя на курс """

        request = self.context.get('request')

        if request is None:
            return False

        user = request.user

        if not user.is_authenticated:
            return False
        return Subscription.objects.filter(user=user, course=instance).exists()

    def get_price(self, instance):
        """ Получение стоимости курса """
        return instance.price


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Курс с подпиской """
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']
