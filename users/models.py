from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length = 20,unique=True)
    password = models.CharField(max_length = 200)
    salt = models.CharField(max_length = 100)
    email = models.CharField(max_length = 50,unique=True)
    is_locked = models.BooleanField(default=False)
    failed_login_tries = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.name
