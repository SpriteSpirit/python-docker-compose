from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.filters import PaymentFilter
from users.models import User, Payment
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer, PublicUserSerializer, \
    PrivateUserSerializer


class RegisterView(APIView):
    """ Регистрация нового пользователя """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    """ Список всех пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Получение информации о конкретном пользователе """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """ Удаление пользователя """
    queryset = User.objects.all()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Обновление профиля пользователя или просмотр профиля в зависимости от прав доступа.
    Класс предоставляет как чтение (GET), так и обновление (PUT, PATCH) объекта.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        """ Получение пользователя. Если пользователь пытается обновить чужой профиль, вызывается исключение """
        if self.request.method in ['PUT', 'PATCH']:
            return self.request.user
        pk = self.kwargs.get('pk')
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="Пользователь не найден")

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора в зависимости от типа запроса.
        Если запрос является безопасным (GET), возвращается UserSerializer,
        который предоставляет полную информацию о пользователе, включая подписки.
        Для обновления (PUT или PATCH) возвращается PrivateUserSerializer.
        """
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializer  # Используем UserSerializer для GET-запросов
        return PrivateUserSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user != instance and not self.request.user.is_staff:
            raise PermissionDenied(
                detail="Вы не можете редактировать этот профиль")
        serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    """ Фильтрация вывода списка платежей для эндпоинта """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    filterset_class = PaymentFilter

    ordering_fields = ('payment_date',)
    ordering = ('payment_date',)
