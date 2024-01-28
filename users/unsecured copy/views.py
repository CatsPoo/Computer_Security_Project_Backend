from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
import json
from users.passwordHandler import WeakPasswordExeption
from users.unsecured.usersHandler import UserIsTakenExeption,EmailIsTakenExeption
import users.unsecured.webActionHandler as webActionHandler
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def test(requst: HttpRequest):
    return HttpResponse('test - users - unsecured')

def login(request: HttpRequest):
    pass

@csrf_exempt
def register(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.register(data['username'],data['password'],data['email'])
            return HttpResponse({})
        
        except WeakPasswordExeption:
            return HttpResponseBadRequest('Weak password')
        except UserIsTakenExeption:
            return HttpResponseBadRequest('This username is taken')
        except EmailIsTakenExeption:
            return HttpResponseBadRequest('This Email address is taken')
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def change_password(request: HttpRequest):
    if(request.method=='PUT'):
        try:
            data = json.loads(request.body)
            webActionHandler.change_password(data['username'],data['old_password'],data['new_password'])
            return HttpRequest({})
        except WeakPasswordExeption:
            return HttpResponseBadRequest('Wrong Cradentials')
    else:
        raise HttpResponseBadRequest('Wrong request method')

def reset_password(request: HttpRequest):
    pass
