from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
import json
from costumers.secured import costumersHandller

# Create your views here.

def add_costumer(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            res = costumersHandller.add_costumer(data['name'],data['email'],data['phone_number'])
            return HttpResponse('Costumer addedd seccesfully')
        except costumersHandller.EmailIsTakenExeption:
            return HttpResponseBadRequest('This costumer already exist')
        except Exception as E:
            print(str(E))
            return HttpResponse('Internal server error',500)

    else:
        return HttpResponseBadRequest('Wrong request method')
 

def get_costumer(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            res = costumersHandller.get_costumer(data['email'])
            return HttpResponse(res)
        except costumersHandller.CostumerDoesntExistExeption:
            return HttpResponseBadRequest('This costumer doesn\'t exists')
        except Exception as E:
            print(str(E))
            return HttpResponse('Internal server error',500)

    else:
        return HttpResponseBadRequest('Wrong request method')
 