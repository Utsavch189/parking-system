from django.urls import path
from .views import LoginView,Register

urlpatterns=[
    path('login',LoginView.as_view(),name='parkingowner login'),
    path('register/<str:parking_area_id>&<str:admin_id>',Register.as_view())
]