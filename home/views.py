from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Credential
# Create your views here.

def home(request):
    return HttpResponse("Portal Home Page")


def authenticate(request,user_name,passowrd):
    try:
        Credential.objects.get(user_name=user_name,password=passowrd)
        return True
    except Credential.DoesNotExist:
        return False
