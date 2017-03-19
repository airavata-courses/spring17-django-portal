from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Credential
import requests
# Create your views here.


def dashboard(request, username=None):
    s = requests.Session()
    print('Request to home page with token - ', s.cookies.get("id_token"))
    return render(request, 'home/dash.html', {"username": username})


def loginpage(request):
    print('Serving login page - ')
    return render(request, 'home/login.html')


def authenticate(request, user_name, password):
    try:
        Credential.objects.get(user_name=user_name,password=password)
        return True
    except Credential.DoesNotExist:
        return False