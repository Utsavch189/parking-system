from django.urls import path
from .views import LoginView,Register,Home

urlpatterns=[
    path('login',LoginView.as_view(),name='parkingowner login'),
    path('register',Register.as_view()),
    path('',Home.as_view())
]