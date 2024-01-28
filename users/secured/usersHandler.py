from django.db import connection
import users.passwordHandler as passwordHandler

def add_user(username,password,email):
    pass

def is_user_exists(username):
    pass

def is_email_exists(email):
    pass


def delete_user(username):
    pass

def change_user_password(username, new_password):
    pass

def forgot_password(username):
    pass

def get_user_salt(username):
    pass
    
def get_user_password(username):
    pass
    
def password_is_currect(username,password):
    pass