from django.urls import path
from .views import (LoginView,HomePageView,GetFacilities,ParkingAreaView,
                    GetParkingAreas,DeleteParkingArea,
                    ConfirmDeleteParkingArea,ProfileView,RegisterView,
                    SearchCountry,ParkingAttendantPage,GetParkingAttendants,
                    DeleteParkingAttendant,ConfirmDeleteParkingAttendant,
                    VerifyParkingAttendant,SuspendParkingAttendant
                    )

urlpatterns=[
    path('login',LoginView.as_view(),name='admin login'),
    path('',HomePageView.as_view(),name='admin home'),
    path('all-facilities',GetFacilities.as_view()),
    path('parking-area',ParkingAreaView.as_view()),
    path('get-parking-areas',GetParkingAreas.as_view()),
    path('delete-parking-area/<str:id>',DeleteParkingArea.as_view()),
    path('delete-confirm-area/<str:admin_id>&<str:area_id>',ConfirmDeleteParkingArea.as_view()),
    path('profile',ProfileView.as_view()),
    path('register',RegisterView.as_view()),
    path('search-country',SearchCountry.as_view()),
    path('parking-attendants',ParkingAttendantPage.as_view()),
    path('get-parking-attendants',GetParkingAttendants.as_view()),
    path('delete-parking-attendant/<str:id>',DeleteParkingAttendant.as_view()),
    path('delete-confirm-attendant/<str:admin_id>&<str:attendant_id>',ConfirmDeleteParkingAttendant.as_view()),
    path('verify-attendant',VerifyParkingAttendant.as_view()),
    path('suspend-attendant',SuspendParkingAttendant.as_view())
]