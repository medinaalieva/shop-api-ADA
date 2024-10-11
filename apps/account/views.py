from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.account.models import UserResetPasswordToken
from apps.account.send_email import send_activation_email, send_password_reset_email
from apps.account.serializers import RegisterSerializer, LogOutSerializer, ResetPasswordSerializer, \
    ResetPasswordConfirmSerializer
from apps.account.utils import generate_reset_password_code

User = get_user_model()


class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            try:
                send_activation_email(email=user.email, code=user.activation_code)
            except Exception as e:
                print(e, '!!!!!!!!!!!!!!!!!!!!!!!!')
                return Response(
                    {
                        'message': 'Во время отправки письма что-то пошло не так!',
                        'data': serializer.data
                    }, status=HTTPStatus.CREATED
                )
            return Response(serializer.data, status=HTTPStatus.CREATED)


class ActivationView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Вы успешно активировали ваш аккаунт', status=HTTPStatus.OK)


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny, ]


class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny, ]


class LogOutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно вышли с аккаунта', 200)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('Такого пользователя не существует', 404)

        reset_code = generate_reset_password_code()
        UserResetPasswordToken.objects.create(user=user, token=reset_code)
        send_password_reset_email(email=email, reset_code=reset_code)
        return Response('Вам на почту отправлено сообщение с инструкцией по сбросу пароля', 200)


class PasswordResetConfirmView(APIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = request.data.get('code')
        new_password = request.data.get('new_password1')

        try:
            reset_code = UserResetPasswordToken.objects.get(token=code)
        except UserResetPasswordToken.DoesNotExist:
            return Response('Неправильный код', 400)

        if not reset_code.is_valid():
            return Response('Код истек')
        user = reset_code.user

        user.set_password(new_password)
        user.save()


        # reset_code.delete()
        return Response('Вы успешно изменили пароль', 200)
