from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserCreateAPIView, UserListAPIView, \
    UserRetrieveAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-get'),
    path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),
]
