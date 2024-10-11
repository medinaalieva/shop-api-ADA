from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegistrationView,
    ActivationView,
    LoginView,
    RefreshView,
    LogOutView,
    ResetPasswordView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('reset_password_confirm/', PasswordResetConfirmView.as_view())
]