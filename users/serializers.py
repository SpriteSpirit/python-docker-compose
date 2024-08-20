from rest_framework import serializers

from lms.models import Subscription
from lms.serializers import SubscriptionSerializer
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """ Сериализатор платежа """

    class Meta:
        model = Payment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации нового пользователя """
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )

        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя """
    payments = PaymentSerializer(source='payment', many=True, read_only=True)
    subscriptions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def get_subscriptions(self, instance):
        subscriptions = Subscription.objects.filter(user=instance)
        print(SubscriptionSerializer(subscriptions, many=True).data)
        return SubscriptionSerializer(subscriptions, many=True).data


class PublicUserSerializer(serializers.ModelSerializer):
    """ Публичный сериализатор """
    class Meta:
        model = User
        exclude = ('password', 'last_name',)  # исключаем чувствительные поля


class PrivateUserSerializer(serializers.ModelSerializer):
    """ Приватный сериализатор """

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'date_joined', 'last_login', 'password')
