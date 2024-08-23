import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """ Фильтрация платежей по дате """
    payment_date = django_filters.DateTimeFilter(field_name='payment_date', lookup_expr='date')
    # фильтрация по дате {{base_url}}/users/payments/?payment_date=2024-08-09

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_date']
