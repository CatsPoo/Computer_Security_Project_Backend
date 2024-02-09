import secrets
import random
from Comunication_LTD.hashHandler import generate_hmac
from django.conf import settings

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

    if(len(password) < settings.Min_PASSWORD_LENGTH): return False

    for c in password:
        if c>= 'a' and c <= 'z':
            has_numbers==True
        if c >= '0' and c <='9':
            has_numbers=True
        if c >= 'A' and c<='Z':
            has_capital_letter =True
        if c in settings.SPEICHAL_CHRECTER_LIST:
            has_speical_letter = True

    if(settings.MUST_HAVE_CAPITAL_LETTERS and not has_capital_letter): return False
    if(settings.MUST_HAVE_SMALL_LETTERS and not has_small_letter): return False
    if(settings.MUST_HAVE_NUMBERS and not has_numbers): return False
    if(settings.MUST_HAVE_SPEICHAL_CHRECTER and not has_capital_letter): return False

    return True


    return True


def is_passwords_mached(clear_text_password,hashed_password,salt):
    return (hash_password(clear_text_password,salt) == hashed_password)

class WeakPasswordExeption(Exception):
    pass

class PasswordAlreadyWasInUse(Exception):
    pass

