from django.contrib import admin
from lms.models import Course, Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'preview', 'last_updated']
    list_filter = ['title']
    search_fields = ['title', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'description', 'preview']
    list_filter = ['course', 'title']
    search_fields = ['course__title', 'title']
