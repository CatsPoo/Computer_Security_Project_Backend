from django.db import connection
from django.db import transaction
from costumers.models import Costumer

def is_costumer_exists(email):
    sql_query = f"select * from costumers_costumer where email= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,email,)
        row = cursor.fetchall()

        if(row): return True
    return False

def add_user(name,email,phone_number):

    sql_query = f"INSERT INTO costumers_costumer (name,email,phone_number) VALUES (%s,%s,%s)"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,(name,email,phone_number))

        row = cursor.fetchone()
        return row


def get_costumer(email):
    sql_query = f"select * from costumers_costumer where email= %s"

    with connection.cursor() as cursor:
        cursor.execute(sql_query,email,)
        row = cursor.fetchone()
        return row


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