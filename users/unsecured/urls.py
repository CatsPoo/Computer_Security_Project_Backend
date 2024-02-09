from django.urls import path, include
from users.unsecured import views
urlpatterns = [
    path('register',views.register),
    path('change_password',views.change_password),
    path('login',views.login),
    path('send_reset_password_email',views.send_reset_password_email),
    path('reset_password',views.reset_password)

    
]