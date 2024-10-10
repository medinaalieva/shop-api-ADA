from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from apps.account.send_email import send_activation_email, send_password_reset_email
from apps.account.serializers import RegisterSerializer, LogOutSerializer, ResetPasswordSerializer

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

