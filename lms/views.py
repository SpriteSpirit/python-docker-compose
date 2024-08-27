from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import LessonSerializer, CourseSerializer, SubscriptionSerializer
from lms.tasks import send_course_update_email
from users.permissions import IsOwnerOrModerator, IsNotModerator


# ViewSet для курса
class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для управления CRUD операциями с курсами """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = CoursePaginator

    def get_permissions(self):
        """ Получение прав """
        if self.action in ['update', 'partial_update']:
            return [IsOwnerOrModerator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """ Фильтрация курсов в зависимости от роли пользователя """
        if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """ Создание курса с присвоением создателя-пользователя """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """ Обновление только своего курса """
        course = get_object_or_404(Course, owner=serializer.instance.owner)
        subscriptions = Subscription.objects.all()

        if self.request.user != serializer.instance.owner:
            raise PermissionDenied('Вы не можете редактировать этот курс.')

        for subscription in subscriptions:
            if subscription.course == course:
                send_course_update_email.delay(subscription.user.email, subscription.course.course)
        serializer.save()

    def perform_destroy(self, instance):
        """ Удаление только своего курса """
        if self.request.user != instance.owner:
            raise PermissionDenied('Вы не можете удалить этот курс.')
        instance.delete()

    def get_serializer_context(self):
        """ Передача контекста запроса в сериализатор """
        return {'request': self.request}


# Generics для уроков
class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """ Создание урока с присвоением создателя-пользователя """
        serializer.save(owner=self.request.user)
        pass


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_permissions(self):
        """ Получение прав """
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsOwnerOrModerator()]
        return super().get_permissions()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр одного урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator]


class SubscriptionCreateView(APIView):
    """ Создание подписки пользователя """

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            message = 'Подписка добавлена'
        else:
            subscription.delete()
            message = 'Подписка удалена'

        return Response({"message": message}, status=status.HTTP_200_OK)


class SubscriptionListView(APIView):
    """ Список подписок пользователя """

    def get_queryset(self):
        """ Фильтрация платежей в зависимости от роли пользователя """
        user = self.request.user

        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return Subscription.objects.all()
        elif user.is_authenticated:
            return Subscription.objects.filter(user=user.pk)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
