from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
import requests


def loginuser(request):
    client_id = settings.IDP_CLIENT_ID
    base_authorize_url = settings.IDP_AUTHORIZE_URL
    redirect_url = 'http://localhost:8080/auth/realms/Airavata/protocol/openid-connect/auth' + '?'
    redirect_url += 'response_type=code&scope=openid&client_id=django&redirect_uri=http%3A%2F%2Flocalhost:8000%2Fauth%2Fvalidate%2F'
    """
    params = {'client_id': client_id, 'scope': base_authorize_url}
    r = requests.post(base_authorize_url, data=params)
    userinfo = r.json()

    Add OAuth calls here
    wso2is = OAuth2Session(client_id, scope='openid',
                           redirect_uri=request.build_absolute_uri(reverse('airavata_auth_callback')))
    authorization_url, state = wso2is.authorization_url(base_authorize_url)
    logger.debug("authorization_url={}, state={}".format(authorization_url, state))
    # Store state in session for later validation
    request.session['OAUTH2_STATE'] = state
    return redirect(authorization_url)
    authenticate(request=request)


    context = {'username': username}
    return render(request, 'home/home.html', context)"""
    return redirect(redirect_url)


def get_token(request):
    code = request.GET.get('code')
    print('Putting Code : ', code, ' in session')
    url = 'http://localhost:8080/auth/realms/Airavata/protocol/openid-connect/token/'
    data = {
        "grant_type":"authorization_code",
        "code": code,
        "redirect_uri": "http%3A%2F%2Flocalhost:8000%2Fhome%2Fdashboard%2F",
        "client_id": "django",
        "client_secret_basic": "72a5898c-3c9b-4cdb-a8e3-db319960bd26"
    }

    '''
    &code=' + code
    redirect_url += "&redirect_uri=http%3A%2F%2Flocalhost:8000%2Fhome%2Fdashboard%2F"
    redirect_url += "client_id=django&client_secret_basic=72a5898c-3c9b-4cdb-a8e3-db319960bd26"

    r = requests.post(url, data=data)
    id_token = requests.Session().cookies.get("id_token")
    print('id_token: ', id_token)
    '''
    return redirect('/home/dashboard/')


def set_token(request):
    id_token = request.GET.get('code')
    s = requests.Session()
    data = {"id_token": id_token}
    url = "http://localhost:8000/home/dashboard"
    s.post(url, data=data)


def logoutuser(request):
    print('Inside logout function')
    return redirect('/home/login/')
