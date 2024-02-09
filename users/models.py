from django.db import models

# Create your models here.

class Passwords_History(models.Model):
    index=models.AutoField(primary_key=True,unique=True)
    password=models.CharField(max_length=200)
class Users(models.Model):
    username = models.CharField(max_length = 20,unique=True)
    password = models.CharField(max_length = 200)
    salt = models.CharField(max_length = 100)
    email = models.CharField(max_length = 50,unique=True)
    is_locked = models.BooleanField(default=False)
    failed_login_tries = models.SmallIntegerField(default=0)
    reset_password_key = models.CharField(max_length=100,default='')
    passwords_history=models.ManyToManyField(Passwords_History)
    def __str__(self) -> str:
        return self.name
    

