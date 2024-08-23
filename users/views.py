import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course
from users.filters import PaymentFilter
from users.models import User, Payment
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer, \
    PrivateUserSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product, \
    get_checkout_session_status


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
        except ObjectDoesNotExist:
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


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание платежа [POST - запрос]"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson')
    filterset_class = PaymentFilter

    ordering_fields = ('payment_date',)
    ordering = ('payment_date',)

    def perform_create(self, serializer):
        """ Обрабатывает создание нового платежа """
        # сохраняет новый платеж в базе данных, используя данные из запроса
        payment = serializer.save(user=self.request.user)
        # создает товар Stripe с именем курса, полученным из запроса
        product = create_stripe_product(serializer.validated_data['course'].title)
        # создает цену Stripe для товара, используя ID товара и стоимость платежа
        price = create_stripe_price(product.id, serializer.validated_data['course'].price)
        # создает сессию Stripe для оплаты, используя ID товара и цену
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        print(f'session_id: {payment.session_id }')
        print(f'payment_link: {payment.link}')

        # Сохранение идентификатора купленного курса в сессию
        self.request.session['purchased_course_id'] = serializer.validated_data['course'].id
        print(self.request.session['purchased_course_id'])
        self.request.session.modified = True
        payment.save()

        return payment


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Проверка статуса платежа """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        # Получаем объект
        instance = self.get_object()

        # Получаем session_id из объекта
        session_id = instance.session_id

        # Проверяем статус через Stripe
        status_message = get_checkout_session_status(session_id)

        # Добавляем статус в исходные данные
        data = self.serializer_class(instance).data
        data['status'] = status_message

        return Response(data)


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей пользователя [GET] """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class SuccessUrlView(TemplateView):
    template_name = "users/success_url.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Получаем session_id из объекта
    #     session = self.request.session
    #     print(session)
    #
    #     # Проверяем статус через Stripe
    #     status_message = get_checkout_session_status(session)
    #     course_id = self.request.session.get('purchased_course_id')
    #     print(status_message)
    #     print(course_id)
    #     print(f"Session data in SuccessUrlView: {self.request.session.items()}")  # Логирование данных сессии
    #     if course_id:
    #         context['course'] = Course.objects.get(pk=course_id)
    #
    #         del self.request.session['purchased_course_id']
    #         self.request.session.modified = True
    #     return context
