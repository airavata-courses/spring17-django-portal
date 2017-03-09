from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Credential
from apache.airavata.api.credentials.CredentialManagementService import Client as CredentialManagementServiceClient
from apache.airavata.api.gateway.management.GatewayManagementService import Client as GatewayManagementServiceClient
from portal.settings import PROTOCOL
from django.core.cache import cache

# Create your views here.

cred_client=CredentialManagementServiceClient(PROTOCOL)
gat_client=GatewayManagementServiceClient(PROTOCOL)

def home(request):
    return HttpResponse("Portal Home Page")


def authenticate(request,user_name,passowrd):
    try:
        Credential.objects.get(user_name=user_name,password=passowrd)
        return True
    except Credential.DoesNotExist:
        return False

def generate_ssh(request):
    key=cred_client.generateAndRegisterSSHKeys("test","test")
    return HttpResponse("Keys generated"+key)


def register_gatway(request):
    name=gat_client.registerGateway(request.GET['gateway'])
    return HttpResponse("Gateway Name: "+ name)
