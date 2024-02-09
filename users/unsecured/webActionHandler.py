import json
import users.passwordHandler as passwordHandler
import users.unsecured.usersHandler as usersHandler
from users import usersExeptions
from django.conf import settings
from django.core.mail import send_mail
import random
from Comunication_LTD.hashHandler import sha1_hash

def register(username,password,email):
    if(not passwordHandler.is_password_valid(password)):
        raise passwordHandler.WeakPasswordExeption
    if(usersHandler.is_user_exists(username)):
        raise usersExeptions.UserIsTakenExeption()
    if(usersHandler.is_email_exists(email)):
        raise usersExeptions.EmailIsTakenExeption()
    
    usersHandler.add_user(username,password,email)

def change_password(username,old_password,new_password):

    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption
    
    if(not passwordHandler.is_password_valid(new_password)):
        raise passwordHandler.WeakPasswordExeption
    
    current_password_on_db = usersHandler.get_user_password(username)
    current_user_salt = usersHandler.get_user_salt(username)

    if(passwordHandler.is_passwords_mached(old_password,current_password_on_db,current_user_salt)):
        usersHandler.change_user_password(username,new_password)
    else:
        raise usersExeptions.WrongCradentialsExeption

def login(username,password):
    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption
    if(usersHandler.get_is_locked_value(username)):
        raise usersExeptions.LockedUserExeption
    
    user_hashed_password = usersHandler.get_user_password(username)
    users_salt = usersHandler.get_user_salt(username)

    if(passwordHandler.is_passwords_mached(user_hashed_password,password,users_salt)):
        return True
    else:
        current_user_failed_trues = usersHandler.get_failed_login_tries(username)
        usersHandler.update_failed_login_tries(username,current_user_failed_trues + 1)

        if(current_user_failed_trues >= settings.MAX_LOGIN_TRIES):
            usersHandler.update_is_lock_value(username,True)
        
        raise usersExeptions.WrongCradentialsExeption
    
def send_reset_password_mail(username,email):
    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption
    
    user_email = usersHandler.get_user_email(username)

    if(user_email != email):
        raise usersExeptions.WrongCradentialsExeption

    rest_password_random_value = str(random.randint(100,9999))
    hased_reset_pasword_random_value = sha1_hash(rest_password_random_value)

    usersHandler.set_user_reset_password_key(username,hased_reset_pasword_random_value)

    send_mail(
    "Reset password",
    "Your secret code is: {hased_reset_pasword_random_value}",
    settings.EMAIL_HOST_USER,
    [user_email],
    fail_silently=False,
    )

def reset_password_mail(username,key,new_password):
    real_user_reset_password_key = usersHandler.get_user_reset_password_key(username)

    if(not passwordHandler.is_password_valid(new_password)):
        raise passwordHandler.WeakPasswordExeption

    if(real_user_reset_password_key == key):
        usersHandler.change_user_password(username,new_password)
    else:
        raise usersExeptions.WrongCradentialsExeption
