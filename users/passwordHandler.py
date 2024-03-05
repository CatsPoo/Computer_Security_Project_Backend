import secrets
import random
from Comunication_LTD.hashHandler import generate_hmac
from django.conf import settings
from  .models import Users, Password
from .secured import  usersHandler
from django.db import connection

def add_password(user_id,password,salt):
    sql_query = "INSERT INTO users_password (user_id,password, salt)VALUES (%s,%s, %s);"
    with connection.cursor() as cursor:
        cursor.execute(sql_query,(user_id,password,salt,))
        row = cursor.fetchone()
        return row
    
def get_passwords(user_id):
    sql_query = "select password from users_password where user_id =  %s;"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,(user_id,))
        row = cursor.fetchall()
        return [i[0] for i in row][::-1]


def hash_password(password,salt):
    return generate_hmac(password, salt)

def generate_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)

def is_password_valid(password):
    has_capital_letter = False
    has_small_letter = False
    has_numbers = False
    has_speical_letter = False

    if(len(password) < settings.MIN_PASSWORD_LENGTH): return False

    for c in password:
        if c >= 'a' and c <= 'z':
            has_small_letter=True
        if c >= '0' and c <='9':
            has_numbers=True
        if c >= 'A' and c<='Z':
            has_capital_letter =True
        if c in settings.SPEICHAL_CHRECTER_LIST:
            has_speical_letter = True

    if(settings.MUST_HAVE_CAPITAL_LETTERS and not has_capital_letter): return False
    if(settings.MUST_HAVE_SMALL_LETTERS and not has_small_letter):  return False
    if(settings.MUST_HAVE_NUMBERS and not has_numbers): return False
    if(settings.MUST_HAVE_SPEICHAL_CHRECTER and not has_speical_letter): return False

    return True

def is_password_available(user_id,password):
    salt = usersHandler.get_user_salt(user_id)
    user_passwords_hist = get_passwords(user_id)
    n_last_passwords = user_passwords_hist[:settings.PASSWORD_HISTORY_COUNT]
    for passwd in n_last_passwords:
        if(is_passwords_mached(password,passwd,salt)):
            return False
    return True

def is_passwords_mached(clear_text_password,hashed_password,salt):
    return (hash_password(clear_text_password,salt) == hashed_password)

class WeakPasswordExeption(Exception):
    pass

class PasswordAlreadyWasInUse(Exception):
    pass

