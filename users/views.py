from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.filters import PaymentFilter
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer


class RegisterView(APIView):
    """ Регистрация нового пользователя """
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserCreateAPIView(generics.CreateAPIView):
#     """ Создание нового пользователя """
#     serializer_class = UserSerializer


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
