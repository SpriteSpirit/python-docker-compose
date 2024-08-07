from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    pass


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer = UserSerializer
    queryset = User.objects.all()
