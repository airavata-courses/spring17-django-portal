from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
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
    print('Putting Code : ', code, ' in cache')
    cache.set('auth_code',code,settings.CACHE_MIDDLEWARE_SECONDS)
    url = settings.IDP_TOKEN_URL
    data = {
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri": settings.HOST_ADDRESS + "auth/validate/",
        "client_id": client_id,
        "client_secret": settings.IDP_CLIENT_SECRET
    }

    token_resp = requests.post(url, data=data)
    if token_resp.status_code != 200:
        print("Error while getting token")

    json_token_resp = token_resp.json()
    id_token = json_token_resp['id_token']
    access_token = json_token_resp['access_token']

    print("Putting id_token and access_token in cache")
    cache.set('id_token', id_token, settings.CACHE_MIDDLEWARE_SECONDS)
    cache.set('access_token', access_token, settings.CACHE_MIDDLEWARE_SECONDS)

    userinfo_resp = requests.get(settings.IDP_USERINFO_URL, headers={"Authorization":"Bearer " + access_token})

    if userinfo_resp.status_code != 200:
        print("Error while getting user info")

    json_userinfo_resp = userinfo_resp.json()
    user_id = json_userinfo_resp['preferred_username']

    print("Logged in ",user_id, " !!")
    cache.set('user_id',user_id, settings.CACHE_MIDDLEWARE_SECONDS)
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
