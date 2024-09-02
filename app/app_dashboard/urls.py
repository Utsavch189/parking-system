from django.urls import path
from .views import DashboardView,AboutView,ContactView,LoginView

urlpatterns=[
    path('',DashboardView.as_view(),name='dashboard'),
    path('about',AboutView.as_view(),name='about'),
    path('contact',ContactView.as_view(),name='contact'),
    path('login',LoginView.as_view(),name='login')
]