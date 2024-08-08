from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets

from users.filters import PaymentFilter
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """ Создание нового пользователя """
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()


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


class PaymentViewSet(viewsets.ModelViewSet):
    """ Фильтрация вывода списка платежей для эндпоинта """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    filterset_class = PaymentFilter

    ordering_fields = ('payment_date',)
    ordering = ('payment_date',)
