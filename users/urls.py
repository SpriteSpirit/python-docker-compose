from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListAPIView, \
    UserDestroyAPIView, PaymentViewSet, RegisterView, UserProfileView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    # path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('update/<int:pk>/', UserProfileView.as_view(), name='user-update'),
    path('', UserListAPIView.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
] + router.urls
