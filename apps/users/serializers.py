from rest_framework import serializers
from .models import User, Mandate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone']

    def validate_password(self, value):
        # (длина, похожесть на email, частые пароли, только цифры)
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        # создаем чтобы пароль сохранился захешированным
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(source='groups', many=True, read_only=True, slug_field='name')
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone','roles']



class MandateSerializer(serializers.ModelSerializer):
    mandant = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Mandate
        fields = ['id', 'mandant', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']

    def validate_mandant(self, value):
        steuerberater = self.context['request'].user
        if value == steuerberater:
            raise serializers.ValidationError('You cannot add yourself as a client.')
        if Mandate.all_objects.filter(steuerberater=steuerberater, mandant=value).exists():
            raise serializers.ValidationError('This client is already added.')
        return value