from django.urls import path, include

urlpatterns = [
    path('unsecured/',include('costumers.unsecured.urls')),
    path('secured/',include('costumers.secured.urls'))
]