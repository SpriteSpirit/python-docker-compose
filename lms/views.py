from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModerator, IsNotModerator


# ViewSet для курса
class CourseViewSet(viewsets.ModelViewSet):
    """ API endpoint для курсов """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

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
        print(serializer)

    def perform_update(self, serializer):
        """ Обновление только своего курса """
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied('Вы не можете редактировать этот курс.')
        serializer.save()

    def perform_destroy(self, instance):
        """ Удаление только своего курса """
        if self.request.user != instance.owner:
            raise PermissionDenied('Вы не можете удалить этот курс.')
        instance.delete()


# Generics для уроков
class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        """ Создание урока с присвоением создателя-пользователя """
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

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
