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
