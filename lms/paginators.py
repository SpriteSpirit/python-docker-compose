from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    """ Разбивка данных урока на страницы """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class CoursePaginator(PageNumberPagination):
    """ Разбивка данных курса на страницы """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 30
