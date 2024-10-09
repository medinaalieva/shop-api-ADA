from os import write

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')

        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпали')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError('Email field is required')
        return email

