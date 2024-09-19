from django.urls import path
from .views import LoginView,Register,Home,SlotView

urlpatterns=[
    path('login',LoginView.as_view(),name='parkingowner login'),
    path('register',Register.as_view()),
    path('',Home.as_view()),
    path('parking-slot',SlotView.as_view())
]