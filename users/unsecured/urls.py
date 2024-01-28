from django.urls import path, include
from users.unsecured import views
urlpatterns = [
    path('test',views.test),
    path('register',views.register),
    path('change_password',views.change_password)
]