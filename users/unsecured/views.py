from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
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
            return JsonResponse({'message':'Authorized'}, status=200)
        except WrongCradentialsExeption:
            return JsonResponse({'error':'Not Authorized'}, status=403)
        except Exception as E:
            print(E)
            return JsonResponse({'error':'Internal Server Error'},status=500)
        
@csrf_exempt
def register(request: HttpRequest):
    if(request.method == 'POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.register(data['username'],data['password'],data['email'])
            return JsonResponse({'message':'Registerd Seccesfully'}, status=200)
        
        except WeakPasswordExeption:
            return JsonResponse({'error':'Weak password'},status=400)
        except UserIsTakenExeption:
            return JsonResponse({'error':'This username is taken'},status=400)
        except EmailIsTakenExeption:
            return JsonResponse({'error':'This Email address is taken'},status=400)
        except Exception as E:
            print(E)
            return JsonResponse({'error':str(E)},status=500)
    else:
        return JsonResponse({'error':'Wrong Request Method'}, status = 400)

@csrf_exempt
def change_password(request: HttpRequest):
    if(request.method=='PUT'):
        try:
            data = json.loads(request.body)
            webActionHandler.change_password(data['username'],data['old_password'],data['new_password'])
            return JsonResponse({'message':"Password Seccessfully Changed"},status=200)
        except WeakPasswordExeption:
            return JsonResponse({'error':'The password is week'},status = 400)
        except WrongCradentialsExeption:
            return JsonResponse({'error':'Wrong Cradentials'},status = 400)
        except PasswordAlreadyWasInUse:
            return JsonResponse({'error':'Password Was In Use'},status = 400)
        except Exception as E:
            print(E)
            return JsonResponse({'error':str(E)},status=500)
    else:
        return JsonResponse({'error':'Wrong request method'},status=400)
    
def send_reset_password_email(request: HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.send_reset_password_mail(data['email'])
            return JsonResponse({'message' :'ok'},status = 200)
        except WrongCradentialsExeption:
            return JsonResponse({'error':'Wrong Cradentials'},status = 400)
        except Exception as E:
            print(E)
            return JsonResponse({'error':'Internal Server Error'},status=500)
    
    else:
        return JsonResponse({'error':'Wrong request method'},status = 400)

def reset_password(request:HttpRequest):
    if(request.method=='POST'):
        try:
            data = json.loads(request.body)
            webActionHandler.reset_password_mail(data['username'],data['key'],data['new_password'])
            return JsonResponse({'message': 'OK'},status = 200)
        except WrongCradentialsExeption:
            return JsonResponse({'error':'Wrong Cradentials'},status = 400)
        except WeakPasswordExeption:
            return JsonResponse({'error':'Week password'},status = 200)
        except Exception as E:
            print(E)
            return JsonResponse({'error':'Internal Server Error'},status=500)
    else:
        return JsonResponse({'error':'Wrong request method'},status = 400)
