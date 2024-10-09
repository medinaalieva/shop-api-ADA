from http import HTTPStatus

from celery.bin.control import status
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.send_email import send_activation_email
from apps.account.serializers import RegisterSerializer


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

