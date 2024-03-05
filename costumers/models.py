from django.db import models

# Create your models here.
class Costumer(models.Model):
    name = models.(max_length = 20)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
