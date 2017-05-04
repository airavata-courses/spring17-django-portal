from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.


@never_cache
@login_required
def tab1(request):
    context = {
        'user': request.user.get_username()
    }
    print("USER: "+request.user.get_username())
    return render(request,"tab1.html",context)