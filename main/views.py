from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

import time


# Create your views here.

tab_list=[
    {
        'url':'/tab1',
        'name':'Credentials Management'
    },
    {
        'url':'/tab2',
        'name':'Gateway Management'
    }
]

context={
    'tab_list':tab_list
}

@csrf_exempt
def main(request):
    return render(request,"main.html",context)

@csrf_exempt
def test_api(request):
    time.sleep(10)
    return HttpResponse('Response')

@never_cache
def login_api(request):
    if not request.user.is_authenticated:
        user=authenticate(username=request.POST.get('user'), password=request.POST.get('pass'))
        if user is not None:
            login(request, user)
            print('Authenticated')
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
    else:
        return JsonResponse({'status':True})

@csrf_exempt
def login_view(request):
    return render(request,'login.html')

@csrf_exempt
@never_cache
def create_user_view(request):
    return render(request,'create_user.html')

@csrf_exempt
def create_user(request):
    try:
        user = User.objects.create_user(request.POST.get('user'), request.POST.get('name'), request.POST.get('pass'))
        user.save()
        return JsonResponse({'status': True})
    except Exception as e:
        return JsonResponse({'status': False})


