from django.db import connection
import users.passwordHandler as passwordHandler
from users.models import Users,Password
from django.db import transaction

def get_user(username):
        return Users.objects.get(username=username)

def add_user(username,password,email):
    salt = passwordHandler.generate_salt()
    hased_password = passwordHandler.hash_password(password,salt)

    with transaction.atomic():
        user = Users.objects.create(username = username,email= email)
        password = passwordHandler.add_password(password=hased_password,salt=salt)
        user.passwords.add(password)
    return user

def is_user_exists(username):
    try:
        user = Users.objects.get(username= username)
        return True
    except Users.DoesNotExist:
        return False

def is_email_exists(email):
    try:
        user = Users.objects.get(email= email)
        return True
    except Users.DoesNotExist:
        return False

def delete_user(username):
    Users.objects.get(username = username).delete()

def change_user_password(username, new_password):
    user = Users.objects.get(username = username)
    user_salt = get_user_salt(username)
    
    hased_password = passwordHandler.hash_password(new_password,user_salt)
    password = passwordHandler.add_password(hased_password,user_salt)
    print(password.password)
    user.passwords.add(password)


def get_user_salt(username):
    passwords = passwordHandler.get_passwords(username)
    return passwords.last().salt
    
def get_user_password(username):
    passwords = passwordHandler.get_passwords(username)
    print(passwords)
    return passwords.last().password

def get_user_password_history(username):
    passwords = passwordHandler.get_passwords(username)
    return passwords

def get_failed_login_tries(username):
    user = Users.objects.get(username=username)
    return user.failed_login_tries

def update_failed_login_tries(username,new_value):
    user = Users.objects.get(username=username)
    user.failed_login_tries = new_value
    user.save()

def get_is_locked_value(username):
    user = Users.objects.get(username=username)
    return user.is_locked
 
def update_is_lock_value(username,new_value):
    user = Users.objects.get(username=username)
    user.is_locked=new_value
    user.save()

def get_user_email(username):
    user = Users.objects.get(username=username)
    return user.email

def get_user_reset_password_key(username):
    user = Users.objects.get(username=username)
    return user.reset_password_key
    
def set_user_reset_password_key(username,key):
    user = Users.objects.get(username=username)
    user.reset_password_key=key
    user.save()

    