import hmac
import hashlib
import secrets
import random

def hash_password(password,salt):
    return generate_hmac(password, salt)


def generate_salt():
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars=[]
    for i in range(16):
        chars.append(random.choice(ALPHABET))
    return "".join(chars)

def generate_hmac(message, salt):
    hashed_message = hmac.new(salt.encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()
    return hashed_message

def vaildate_password(password):
    return None

def is_passwords_mached(clear_text_password,hashed_password,salt):
    return (hash_password(clear_text_password,salt) == hash_password)

class WeakPasswordExeption(Exception):
    pass

