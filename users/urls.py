from django.urls import path, include

urlpatterns = [
    path('unsecured/',include('users.unsecured.urls')),
    path('secured/',include('users.secured.urls'))
]