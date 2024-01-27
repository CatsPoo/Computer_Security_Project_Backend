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



def login(usename,password):
    pass