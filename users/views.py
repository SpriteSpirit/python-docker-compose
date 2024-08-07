from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer


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
