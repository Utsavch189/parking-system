from django.urls import path,include

urlpatterns=[
    path('',include('app.app_dashboard.urls')),
    path('auth/',include('app.app_auth.urls')),
    path('admins/',include('app.app_admin.urls')),
    path('super-admin/',include('app.app_superadmin.urls')),
    path('sub-admin/',include('app.app_subadmin.urls')),
    path('parking-owner/',include('app.app_parkingowner.urls')),
    # path('users/',include('app.app_parkingowner.urls'))
]