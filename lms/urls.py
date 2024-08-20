from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

from lms.views import CourseViewSet, SubscriptionView
from lms.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('subscriptions/', SubscriptionView.as_view(), name='subscription'),
] + router.urls
