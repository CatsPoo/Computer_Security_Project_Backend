import json
import users.passwordHandler as passwordHandler
import users.unsecured.usersHandler as usersHandler

def register(username,password,email):
    passwordHandler.vaildate_password(password)
    if(usersHandler.is_user_exists(username)):
        raise usersHandler.UserIsTakenExeption()
    if(usersHandler.is_email_exists(email)):
        raise usersHandler.EmailIsTakenExeption()
    
    usersHandler.add_user(username,password,email)

def change_password(username,old_password,new_password):

    if(not usersHandler.is_user_exists(username)):
        raise usersHandler.WrongCradentialsExeption
    
    passwordHandler.vaildate_password(new_password)
    
    current_password_on_db = usersHandler.get_user_password(username)
    current_user_salt = usersHandler.get_user_salt(username)

    if(passwordHandler.is_passwords_mached(old_password,current_password_on_db,current_user_salt)):
        usersHandler.change_user_password(username,new_password)
    else:
        raise usersHandler.WrongCradentialsExeption

def login(usename,password):
    pass