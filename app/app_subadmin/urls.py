from django.urls import path
from .views import LoginView,RegisterView,Home

urlpatterns=[
    path('login',LoginView.as_view(),name='subadmin login'),
    path('register/<str:admin_id>',RegisterView.as_view()),
    path('',Home.as_view())
]