from django.urls import path
from api.v1.auths.views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    ForgetPasswordView,
    OTPSendView,
    OTPVerifyView,
    TwoFactorCreateView,
    TwoFactorVerifyView
)

urlpatterns=[
    path('auth/register',RegisterView.as_view()),
    path('auth/login',LoginView.as_view()),
    path('auth/refresh-token',RefreshTokenView.as_view()),
    path('auth/forget-password',ForgetPasswordView.as_view()),
    path('auth/otp/send',OTPSendView.as_view()),
    path('auth/otp/verify',OTPVerifyView.as_view()),
    path('auth/2fa/create',TwoFactorCreateView.as_view()),
    path('auth/2fa/verify',TwoFactorVerifyView.as_view()),
]