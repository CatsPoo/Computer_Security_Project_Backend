from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
import json
from users.passwordHandler import WeakPasswordExeption,PasswordAlreadyWasInUse
from users.usersExeptions import UserIsTakenExeption,EmailIsTakenExeption,WrongCradentialsExeption
import users.unsecured.webActionHandler as webActionHandler
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def login(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.login(data['username'],data['password'])
            return HttpResponse('Authorized', status=200)
        except WrongCradentialsExeption:
            return HttpResponse('Not Authorized', status=403)
        except Exception as E:
            print(E)
            return HttpResponse('Internal Server Error',status=500)
        
@csrf_exempt
def register(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.register(data['username'],data['password'],data['email'])
            return HttpResponse({'message':'Registerd Seccesfully'}, status=200)
        
        except WeakPasswordExeption:
            return HttpResponseBadRequest({'message':'Weak password'})
        except UserIsTakenExeption:
            return HttpResponseBadRequest({'message':'This username is taken'})
        except EmailIsTakenExeption:
            return HttpResponseBadRequest({'message':'This Email address is taken'})
        except Exception as E:
            print(E)
            return HttpResponse({'message':'Internal Server Error'},status=500)
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def change_password(request: HttpRequest):
    if(request.method=='PUT'):
        try:
            data = json.loads(request.body)
            webActionHandler.change_password(data['username'],data['old_password'],data['new_password'])
            return HttpResponse("Password Seccessfully Changed")
        except WeakPasswordExeption:
            return HttpResponseBadRequest('The password is week')
        except WrongCradentialsExeption:
            return HttpResponseBadRequest('Wrong Cradentials')
        except PasswordAlreadyWasInUse:
            return HttpResponseBadRequest('Password Was In Use')
        except Exception as E:
            print(E)
            return HttpResponse(str(E),status=500)
    else:
        return HttpResponseBadRequest('Wrong request method')
    
@csrf_exempt
def send_reset_password_email(request: HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.send_reset_password_mail(data['username'],data['email'])
            return HttpRequest({})
        except WrongCradentialsExeption:
            return HttpResponseBadRequest('Wrong Cradentials')
        except Exception as E:
            print(E)
            return HttpResponse(str(E),status=500)
    
    else:
        return HttpResponseBadRequest('Wrong request method')

@csrf_exempt
def reset_password(request:HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.reset_password_mail(data['username'],data['key'],data['new_password'])
            return HttpRequest({})
        except WrongCradentialsExeption:
            return HttpResponseBadRequest('Wrong Cradentials')
        except WeakPasswordExeption:
            return HttpResponseBadRequest('Week password')
        except Exception as E:
            print(E)
            return HttpResponse(str(E),status=500)
    else:
        return HttpResponseBadRequest('Wrong request method')
