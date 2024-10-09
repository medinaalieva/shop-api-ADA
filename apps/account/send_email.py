from django.core.mail import send_mail

def send_activation_email(email, code):
    activation_url = f'http://localhost:8000/account/activate/?u={code}'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Для активации аккаунта нужно перейти по ссылке ниже:'
        f'\n{activation_url}',
        'ngrebnev17@gmail.com',
        [email],
        fail_silently=False
    )


def send_password_reset_email(email, user_id):
    password_reset_url = f'http://localhost:8000/account/password_confirm/{user_id}'
    send_mail(
        'Сброс пароля',
        f'Чтобы восстановить пароль, нужно перейти по ссылке'
        f'\n{password_reset_url}',
        'ngrebnev17@gmail.com',
        [email],
        fail_silently=False
    )