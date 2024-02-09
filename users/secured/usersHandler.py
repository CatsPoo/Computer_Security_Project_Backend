from django.db import connection
import users.passwordHandler as passwordHandler
from users.models import Users,Passwords_History
from django.db import transaction

def add_user(username,password,email):
    salt = passwordHandler.generate_salt()
    hased_password = passwordHandler.hash_password(password,salt)

    with transaction.atomic():
        user = Users.objects.create(username = username, password=hased_password,email= email,salt=salt)
        password_hist = Passwords_History.objects.create(password=hased_password,user=user)
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

    with transaction.atomic():
        hased_password = passwordHandler.hash_password(new_password,user.salt)
        user.password = hased_password
        password_hist = Passwords_History(password=hased_password)
        user.passwords_history.aadd(password_hist)
        user.save()


def get_user_salt(username):
    user = Users.objects.get(username=username)
    return user.salt
    
def get_user_password(username):
    user = Users.objects.get(username=username)
    return user.password

def get_user_password_history(username):
    user_passwords = Passwords_History.objects.order_by('index').get(username=username)

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

    