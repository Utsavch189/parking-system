from django.urls import path
from .views import LogoutView,ResetPassword

urlpatterns=[
    path('logout',LogoutView.as_view()),
    path('reset-password',ResetPassword.as_view())
]