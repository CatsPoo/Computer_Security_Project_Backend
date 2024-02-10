import secrets
import random
from Comunication_LTD.hashHandler import generate_hmac
from django.conf import settings
from  .models import Users, Password
from .secured import  usersHandler

def add_password(password,salt):
    password = Password(password = password,salt=salt)
    password.save()
    return Password.objects.order_by('index').last()

def get_passwords(username):
    passwords = Password.objects.filter(users__username = username).order_by('index')
    return passwords


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

def is_password_available(username,password):
    salt = usersHandler.get_user_salt(username)
    user_passwords_hist = get_passwords(username).order_by('-index')
    n_last_passwords = user_passwords_hist[:settings.PASSWORD_HISTORY_COUNT]
    for passwd in n_last_passwords:
        if(is_passwords_mached(password,passwd.password,salt)):
            return False
    return True

def is_passwords_mached(clear_text_password,hashed_password,salt):
    return (hash_password(clear_text_password,salt) == hashed_password)

class WeakPasswordExeption(Exception):
    pass

class PasswordAlreadyWasInUse(Exception):
    pass

