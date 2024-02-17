from django.db import connection
import users.passwordHandler as passwordHandler
def add_user(username,password,email):
    
    new_user_salt = passwordHandler.generate_salt()
    hashed_password = passwordHandler.hash_password(password,new_user_salt)

    sql_query1 = f"INSERT INTO users_users (username,email,is_locked,failed_login_tries,reset_password_key)VALUES (\"{username}\", \"{email}\", \"{False}\",\"0\",\"\");"
    sql_quer2 = f"INSERT INTO users_password (password, salt)VALUES (\"{hashed_password}\", \"{new_user_salt}\");"

    with connection.cursor() as cursor:
        cursor.execute(sql_query1)
        cursor.execute("SELECT last_insert_rowid()")
        user_index = cursor.fetchone()[0]  # Fetch the ID from the result
        cursor.execute(sql_quer2)
        cursor.execute("SELECT last_insert_rowid()")
        password_index = cursor.fetchone()[0] 
        sql_quer3 = f"INSERT INTO users_users_passwords (users_id, password_id)VALUES (\"{user_index}\", \"{password_index}\");"
        cursor.execute(sql_quer3)


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

def get_failed_login_tries(username):
    sql_query = f"select failed_login_tries from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def update_failed_login_tries(username,new_value):
    sql_query = f"update users_users set failed_login_tries=\"{new_value}\" where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row
    

def get_is_locked_value(username):
    sql_query = f"select is_locked from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def update_is_lock_value(username,new_value):
    sql_query = f"update users_users set is_locked=\"{new_value}\"\" where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row

def get_user_email(username):
    sql_query = f"select email from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def get_user_reset_password_key(username):
    sql_query = f"select reset_password_key from users_users where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row[0]
    
def set_user_reset_password_key(username,key):
    sql_query = f"update users_users set reset_password_key=\"{key}\" where username=\"{username}\""

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        row = cursor.fetchone()
        return row