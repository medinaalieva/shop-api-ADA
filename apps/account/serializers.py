from rest_framework import serializers
from django.contrib.auth import get_user_model


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


class ResetPasswordConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(min_length=8, write_only=True, required=True)
    new_password2 = serializers.CharField(min_length=8, write_only=True, required=True)
    code = serializers.CharField(max_length=4, required=True)

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.pop('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError('Пароли не совпали')
        return attrs
