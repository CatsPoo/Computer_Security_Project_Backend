from django.http import HttpRequest
from django.shortcuts import render

def angular_app(request:HttpRequest):
    if(request.method == 'GET'):
        return render(request, 'index.html')
