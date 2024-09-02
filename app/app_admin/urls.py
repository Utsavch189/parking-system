from django.urls import path
from .views import (LoginView,HomeView,GetFacilities,ParkingAreaView,
                    GetParkingAreas,DeleteParkingArea,
                    ConfirmDeleteParkingArea,ProfileView,RegisterView,
                    SearchCountry
                    )

urlpatterns=[
    path('login',LoginView.as_view(),name='admin login'),
    path('',HomeView.as_view(),name='admin home'),
    path('all-facilities',GetFacilities.as_view()),
    path('parking-area',ParkingAreaView.as_view()),
    path('get-parking-areas',GetParkingAreas.as_view()),
    path('delete-parking-area/<str:id>',DeleteParkingArea.as_view()),
    path('delete-confirm-area/<str:admin_id>&<str:area_id>',ConfirmDeleteParkingArea.as_view()),
    path('profile',ProfileView.as_view()),
    path('register',RegisterView.as_view()),
    path('search-country',SearchCountry.as_view())
]