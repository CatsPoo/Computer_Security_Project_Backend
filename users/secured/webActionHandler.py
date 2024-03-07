import json
import users.passwordHandler as passwordHandler
import users.secured.usersHandler as usersHandler
from users import usersExeptions
from django.conf import settings
import random
from Comunication_LTD.hashHandler import sha1_hash
import Comunication_LTD.smtp as mail

def register(username,password,email):
    if(not passwordHandler.is_password_valid(password)):
        raise passwordHandler.WeakPasswordExeption
    if(usersHandler.is_user_exists(username)):
        raise usersExeptions.UserIsTakenExeption()
    if(usersHandler.is_email_exists(email)):
        raise usersExeptions.EmailIsTakenExeption()
    
    usersHandler.add_user(username,password,email)

def change_password(username,old_password,new_password):

    user_id = usersHandler.get_user_id(username)

    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption
    if(not passwordHandler.is_password_valid(new_password)):
        raise passwordHandler.WeakPasswordExeption

    if(not passwordHandler.is_password_available(user_id,new_password)):
        raise passwordHandler.PasswordAlreadyWasInUse
    
    current_password_on_db = usersHandler.get_user_password(user_id)
    current_user_salt = usersHandler.get_user_salt(user_id)

    hased_password = passwordHandler.hash_password(old_password,current_user_salt)

    if(current_password_on_db == hased_password):
        usersHandler.change_user_password(user_id,new_password)
    else:
        raise usersExeptions.WrongCradentialsExeption

def login(username,password):
    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption
    if(usersHandler.get_is_locked_value(username)):
        raise usersExeptions.LockedUserExeption
    
    user_id = usersHandler.get_user_id(username)
    user_hashed_password = usersHandler.get_user_password(user_id)
    users_salt = usersHandler.get_user_salt(user_id)

    if(passwordHandler.is_passwords_mached(password,user_hashed_password,users_salt)):
        usersHandler.update_failed_login_tries(username,0)
        return True
    else:
        current_user_failed_trues = usersHandler.get_failed_login_tries(username)
        usersHandler.update_failed_login_tries(username,current_user_failed_trues + 1)

        if(current_user_failed_trues >= settings.MAX_LOGIN_TRIES):
            usersHandler.update_is_lock_value(username,True)
        
        raise usersExeptions.WrongCradentialsExeption
    
def send_reset_password_mail(email):

    if(not usersHandler.is_email_exists(email)):
        raise usersExeptions.WrongCradentialsExeption

    rest_password_random_value = str(random.randint(1000,9999))
    hased_reset_pasword_random_value = sha1_hash(rest_password_random_value)

    usersHandler.set_user_reset_password_key(email,hased_reset_pasword_random_value)

    mail.send_email('example@sender.local',email,'Reset password key',f'Your reset password key: {hased_reset_pasword_random_value}')

def reset_password_mail(username,key,new_password):
    if(not usersHandler.is_user_exists(username)):
        raise usersExeptions.WrongCradentialsExeption

    real_user_reset_password_key = usersHandler.get_user_reset_password_key(username)
    if(not passwordHandler.is_password_valid(new_password)):
        raise passwordHandler.WeakPasswordExeption
    if(not passwordHandler.is_password_available(new_password)):
        raise passwordHandler.PasswordAlreadyWasInUse
    if(real_user_reset_password_key == key):
        user_id = usersHandler.get_user_id(username)
        usersHandler.change_user_password(user_id,new_password)
        email = usersHandler.get_user_email(username)
        usersHandler.set_user_reset_password_key(email,'')
    else:
        raise usersExeptions.WrongCradentialsExeption
