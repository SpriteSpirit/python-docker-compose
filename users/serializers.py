from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор платежа """

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя """
    payments = PaymentSerializer(source='payment', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
