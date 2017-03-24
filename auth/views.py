from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
import requests, json


def loginuser(request):
    client_id = settings.IDP_CLIENT_ID
    idp_authorize_url = settings.IDP_AUTHORIZE_URL
    redirect_url = idp_authorize_url + '?'
    redirect_url += \
        'response_type=code&scope=openid&' \
        'client_id='+client_id + \
        '&redirect_uri=' + settings.HOST_ADDRESS + 'auth/validate/'
    return redirect(redirect_url)


def get_token(request):
    client_id = settings.IDP_CLIENT_ID
    code = request.GET.get('code')
    print('Putting Code : ', code, ' in session')
    url = settings.IDP_TOKEN_URL
    data = {
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri": settings.HOST_ADDRESS + "auth/validate/",
        "client_id": client_id,
        "client_secret": settings.IDP_CLIENT_SECRET
    }

    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Error while getting token")

    json_resp = response.json()
    print("id_token =", json_resp['id_token'])
    return redirect('/home/dashboard/')


def set_token(request):
    id_token = request.GET.get('code')
    s = requests.Session()
    data = {"id_token": id_token}
    url = settings.HOST_ADDRESS + "home/dashboard"
    s.post(url, data=data)


def logout_user(request):
    end_session_endpoint = \
        settings.IDP_END_SESSION_URL +\
        "?redirect_uri=" + settings.HOST_ADDRESS + "home/login/"
    print('Logging out user')
    return redirect(end_session_endpoint)
