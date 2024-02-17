from django.db import connection
import users.passwordHandler as passwordHandler
from users.models import Users,Password
from django.db import transaction


def add_user(username,password,email):
    new_user_salt = passwordHandler.generate_salt()
    hashed_password = passwordHandler.hash_password(password,new_user_salt)

    sql_query1 = "INSERT INTO users_users (username,email,is_locked,failed_login_tries,reset_password_key)VALUES (%s, %s, False,0,\"\");"
    sql_quer2 = "INSERT INTO users_password (password, salt)VALUES (%s, %s);"

    with connection.cursor() as cursor:
        cursor.execute(sql_query1,(username,email,))
        cursor.execute("SELECT last_insert_rowid()")
        user_index = cursor.fetchone()[0]  # Fetch the ID from the result
        cursor.execute(sql_quer2,(hashed_password,new_user_salt,))
        cursor.execute("SELECT last_insert_rowid()")
        password_index = cursor.fetchone()[0] 
        sql_quer3 = f"INSERT INTO users_users_passwords (users_id, password_id)VALUES (%s, %s);"
        cursor.execute(sql_quer3,(user_index,password_index,))

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
    
def get_user_id(username):
   return get_one_property_of_user(username,'id')[0][0]

def change_user_password(username, new_password):
    user_id = get_user_id(username)
    user_salt = get_user_salt(username)
    
    hased_password = passwordHandler.hash_password(new_password,user_salt) 

    sql_quer2 = "INSERT INTO users_password (password, salt)VALUES (%s, %s);"

    with connection.cursor() as cursor:
        cursor.execute(sql_quer2,(hased_password,user_salt,))
        cursor.execute("SELECT last_insert_rowid()")
        password_index = cursor.fetchone()[0] 
        sql_quer3 = f"INSERT INTO users_users_passwords (users_id, password_id)VALUES (%s, %s);"
        cursor.execute(sql_quer3,(user_id,password_index,))


def get_user_salt(username):
    passwords = passwordHandler.get_passwords(username)
    return passwords.last().salt
    
def get_user_password(username):
    passwords = passwordHandler.get_passwords(username)
    print(passwords)
    return passwords.last().password

def get_user_password_history(username):
    return get_one_property_of_user('password_history')

def get_failed_login_tries(username):
    return get_one_property_of_user(username,'failed_login_tries')[0]

    

def update_failed_login_tries(username,new_value):
    user = Users.objects.get(username=username)
    user.failed_login_tries = new_value
    user.save()

def get_is_locked_value(username):
    return get_one_property_of_user(username,'is_locked')[0][0]
 
def update_is_lock_value(username,new_value):
    user = Users.objects.get(username=username)
    user.is_locked=new_value
    user.save()

def get_user_email(username):
    return get_one_property_of_user(username,'email')[0][0]

def get_user_reset_password_key(username):
    return get_one_property_of_user(username,'reset_password_key')[0][0]
    
def set_user_reset_password_key(username,key):
    user = Users.objects.get(username=username)
    user.reset_password_key=key
    user.save()

    