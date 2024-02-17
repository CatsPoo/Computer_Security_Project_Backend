from django.urls import path, include
from costumers.secured import views
urlpatterns = [
    path('add_costumer',views.add_costumer),
    path('get_costumer',views.get_costumer)
]