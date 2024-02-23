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
            return HttpResponse({'message':'Authorized'}, status=200)
        except WrongCradentialsExeption:
            return HttpResponse({'error':'Not Authorized'}, status=403)
        except Exception as E:
            print(E)
            return HttpResponse({'error':'Internal Server Error'},status=500)
        
@csrf_exempt
def register(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.register(data['username'],data['password'],data['email'])
            return HttpResponse(json.dumps({'message':'Registerd Seccesfully'}), status=200)
        
        except WeakPasswordExeption:
            return HttpResponseBadRequest({'error':'Weak password'})
        except UserIsTakenExeption:
            return HttpResponseBadRequest({'error':'This username is taken'})
        except EmailIsTakenExeption:
            return HttpResponseBadRequest({'error':'This Email address is taken'})
        except Exception as E:
            print(E)
            return HttpResponse({'error':str(E)},status=500)
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def change_password(request: HttpRequest):
    if(request.method=='PUT'):
        try:
            data = json.loads(request.body)
            webActionHandler.change_password(data['username'],data['old_password'],data['new_password'])
            return HttpResponse({'message':"Password Seccessfully Changed"})
        except WeakPasswordExeption:
            return HttpResponseBadRequest({'error':'The password is week'})
        except WrongCradentialsExeption:
            return HttpResponseBadRequest({'error':'Wrong Cradentials'})
        except PasswordAlreadyWasInUse:
            return HttpResponseBadRequest({'error':'Password Was In Use'})
        except Exception as E:
            print(E)
            return HttpResponse({'error':str(E)},status=500)
    else:
        return HttpResponseBadRequest({'error':'Wrong request method'})
    
@csrf_exempt
def send_reset_password_email(request: HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.send_reset_password_mail(data['username'],data['email'])
            return HttpRequest({'message':'OK'})
        except WrongCradentialsExeption:
            return HttpResponseBadRequest({'error':'Wrong Cradentials'})
        except Exception as E:
            print(E)
            return HttpResponse({'error':str(E)},status=500)
    
    else:
        return HttpResponseBadRequest({'error':'Wrong request method'})

@csrf_exempt
def reset_password(request:HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.reset_password_mail(data['username'],data['key'],data['new_password'])
            return HttpRequest({'message':'OK'})
        except WrongCradentialsExeption:
            return HttpResponseBadRequest({'error':'Wrong Cradentials'})
        except WeakPasswordExeption:
            return HttpResponseBadRequest({'error':'Week password'})
        except Exception as E:
            print(E)
            return HttpResponse({'error':str(E)},status=500)
    else:
        return HttpResponseBadRequest({'error':'Wrong request method'})
