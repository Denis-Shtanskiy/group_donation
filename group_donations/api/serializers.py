from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils import timezone
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from collect_payments.models import Collect, Payment, Reason

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для кастомной модели пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'surname',
            'email',
        )


class CreateCustomUserSerializer(UserCreateSerializer):
    """Сериализатор для создания кастомной модели пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'surname',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'surname': {'required': True}
        }


class ReasonCreateSerializer(serializers.ModelSerializer):
    """Сериазатор создания своей причины сборов."""

    class Meta:
        model = Reason
        fields = (
            'id',
            'name',
        )


class ReasonSerializer(serializers.ModelSerializer):
    """Сериализатор причины сборов,
    используется на чтение в других сериализаторах.
    """

    class Meta:
        model = Reason
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class CollectSerializer(serializers.ModelSerializer):
    """Сериализатор сборов, дополнительно подмешиваются донатеры,
    для ленты сборов.
    """

    reason = ReasonSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    payments = serializers.SerializerMethodField()
    cover_image = Base64ImageField()

    class Meta:
        model = Collect
        fields = (
            'id',
            'name',
            'reason',
            'author',
            'description',
            'planned_amount',
            'cover_image',
            'end_date',
            'pub_date',
            'payments',
        )
        read_only_fields = (
            'payments',
        )

    def get_payments(self, obj):
        payments = obj.payment.values(
            'id',
            'amount',
            'created_at',
            full_name=F('user__first_name user__last_name'),
        )
        return payments

    def validate_end_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Выберете дату в будущем!'
            )
        return value


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежей по сбору."""

    class Meta:
        model = Payment
        fields = (
            'user',
            'amount',
            'comments',
            'created_at',
            'collect',
        )
