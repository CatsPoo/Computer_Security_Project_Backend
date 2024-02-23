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
            return HttpResponse({'message':'Costumer addedd seccesfully'},status = 200)
        except costumersHandller.EmailIsTakenExeption:
            return HttpResponseBadRequest({'error':'This costumer already exist'},status = 400)
        except Exception as E:
            print(str(E))
            return HttpResponse({'error' :'Internal server error'},status = 500)

    else:
        return HttpResponseBadRequest({'error' :'Wrong request method'},status = 200)
 

def get_costumer(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            res = costumersHandller.get_costumer(data['email'])
            return HttpResponse({'message' :res},status = 200)
        except costumersHandller.CostumerDoesntExistExeption:
            return HttpResponseBadRequest({'error' :'This costumer doesn\'t exists'},status = 400)
        except Exception as E:
            print(str(E))
            return HttpResponse({'error' :'Internal server error'},500)

    else:
        return HttpResponseBadRequest({'error' :'Wrong request method'})
 