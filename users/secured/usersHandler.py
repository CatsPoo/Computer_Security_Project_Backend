from django.db import connection
import users.passwordHandler as passwordHandler
from users.models import Users,Password
from django.db import transaction


def add_user(username,password,email):
    new_user_salt = passwordHandler.generate_salt()
    hashed_password = passwordHandler.hash_password(password,new_user_salt)

    sql_query1 = "INSERT INTO users_users (username,email,is_locked,failed_login_tries,reset_password_key)VALUES (%s, %s, False,0,\"\");"

    with connection.cursor() as cursor:
        cursor.execute(sql_query1,(username,email,))
        cursor.execute("SELECT last_insert_rowid()")
        user_index = cursor.fetchone()[0]  # Fetch the ID from the result
        passwordHandler.add_password(user_index,hashed_password,new_user_salt)

def is_user_exists(username):
    sql_query = f"select * from users_users where username= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,(username,))
        row = cursor.fetchone()

        if(row): return True
    return False


def is_email_exists(email):
    sql_query = f"select * from users_users where email= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,(email,))
        row = cursor.fetchall()

        if(row): return True
    return False

def get_one_property_of_user(username,field):
    sql_query = f"select {field} from users_users where username= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query, (username,))
        row = cursor.fetchall()
        return row


def update_one_property_of_user(username,field,value):
    sql_query = f"update users_users set {field} = %s where username= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query, (value,username,))
        row = cursor.fetchall()
        return row

def get_user_id(username):
   return get_one_property_of_user(username,'id')[0][0]

def change_user_password(user_id, new_password):
    user_salt = get_user_salt(user_id)
    print(user_salt)
    hased_password = passwordHandler.hash_password(new_password,user_salt)
    passwordHandler.add_password(user_id,hased_password,user_salt)


def get_user_salt(user_id):
    sql_quer2 = "select salt from  users_password where user_id = %s;"

    with connection.cursor() as cursor:
        cursor.execute(sql_quer2,(user_id,))
        return cursor.fetchone()[0]
    

def get_username_by_email(email):
    sql_query = f"select username from users_users where username= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,(email,))
        row = cursor.fetchone()

        return row[0]

def get_user_password(user_id):
    return passwordHandler.get_passwords(user_id)[0]
    

def get_failed_login_tries(username):
    return get_one_property_of_user(username,'failed_login_tries')[0][0]

    

def update_failed_login_tries(username,new_value):
    update_one_property_of_user(username,'failed_login_tries',new_value)

def get_is_locked_value(username):
    return get_one_property_of_user(username,'is_locked')[0][0]
 
def update_is_lock_value(username,new_value):
    update_one_property_of_user(username,'is_locked',new_value)

def get_user_email(username):
    return get_one_property_of_user(username,'email')[0][0]

def get_user_reset_password_key(username):
    return get_one_property_of_user(username,'reset_password_key')[0][0]
    
def set_user_reset_password_key(email,key):
    username = get_username_by_email(email)
    update_one_property_of_user(username,'reset_password_key',key)

    