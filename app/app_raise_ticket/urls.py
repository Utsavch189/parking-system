from django.urls import path
from .views import RaiseTicketPage

urlpatterns=[
    path('',RaiseTicketPage.as_view())
]