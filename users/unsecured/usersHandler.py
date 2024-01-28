from django.db import connection
import users.passwordHandler as passwordHandler
def add_user(username,password,email):
    
    new_user_salt = passwordHandler.generate_salt()
    hashed_password = passwordHandler.hash_password(password,new_user_salt)

    sql_query = f"INSERT INTO users_users (username, password, salt, email)VALUES (\"{username}\", \"{hashed_password}\", \"{new_user_salt}\", \"{email}\");"
    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()

def is_user_exists(username):
    sql_query = f"select * from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()

        if(row): return True
    return False

def is_email_exists(email):
    sql_query = f"select * from users_users where email=\"{email}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()

        if(row): return True
    return False


def delete_user(username):

    sql_query = f"delete from users_users where username={username}"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()

def change_user_password(username, new_password):
    new_user_salt = passwordHandler.generate_salt()
    hashed_new_password = passwordHandler.hash_password(new_password,new_user_salt)
    sql_query = f"update users_users set password=\"{hashed_new_password}\", salt=\"{new_user_salt}\" where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row

def forgot_password(username):
    pass

def get_user_salt(username):
    sql_query = f"select salt from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def get_user_password(username):
    sql_query = f"select password from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def password_is_currect(username,password):
    user_salt = get_user_salt(username)
    user_real_password = get_user_password(username)

    return (passwordHandler.hash_password(password,user_salt) == user_real_password)