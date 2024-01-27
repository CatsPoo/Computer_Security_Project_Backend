from django.urls import path, include

urlpatterns = [
    path('unsecured/',include('users.unsecured.urls'))
]