from django.db import connection
from django.db import transaction
from costumers.models import Costumer

def add_costumer(name,email,phone_number):
    if(not is_email_exists(email)):
        costumer = Costumer(name = name , email = email, phone_number = phone_number)
        costumer.save()
    else:
        raise EmailIsTakenExeption

def get_costumer(email):
    costumer = Costumer.objects.get(email=email)
    return costumer


def is_email_exists(email):
    try:
        costumer = Costumer.objects.get(email= email)
        return True
    except Costumer.DoesNotExist:
        return False

class EmailIsTakenExeption(Exception):
    pass

class CostumerDoesntExistExeption(Costumer.DoesNotExist):
    pass