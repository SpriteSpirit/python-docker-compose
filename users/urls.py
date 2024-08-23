from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIView, \
    UserDestroyAPIView, PaymentCreateView, RegisterView, UserProfileView, SuccessUrlView

app_name = UsersConfig.name

router = DefaultRouter()
# router.register(r'payments', PaymentCreateView, basename='payments')

urlpatterns = [
    path('update/<int:pk>/', UserProfileView.as_view(), name='user-update'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
    path("payments/", PaymentCreateView.as_view(), name='payment'),
    path("success_url/", SuccessUrlView.as_view(), name='success_url'),
] + router.urls
