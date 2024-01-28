from django.db import connection
import users.passwordHandler as passwordHandler
from users.models import Users
def add_user(username,password,email):
    salt = passwordHandler.generate_salt()
    hased_password = passwordHandler.hash_password(password,salt)

    user = Users(username = username, password=hased_password,email= email)
    user.save()
    return user

def is_user_exists(username):
    try:
        user = Users.objects.get(username= username)
        return False
    except Users.DoesNotExist:
        return True

def is_email_exists(email):
    try:
        user = Users.objects.get(email= email)
        return False
    except Users.DoesNotExist:
        return True


def delete_user(username):
    Users.objects.get(username = username).delete()

def change_user_password(username, new_password):
    user = Users.objects.get(username = username)
    user.password = new_password
    user.save()

def forgot_password(username):
    pass

def get_user_salt(username):
    user = Users.objects.get(username=username)
    return user.salt
    
def get_user_password(username):
    user = Users.objects.get(username=username)
    return user.password
    