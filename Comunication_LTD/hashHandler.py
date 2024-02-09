import hmac
import hashlib

def generate_hmac(message, salt):
    hashed_message = hmac.new(salt.encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()
    return hashed_message

def sha1_hash(message):
    return hashlib.sha1(message.encode('utf-8')).hexdigest()