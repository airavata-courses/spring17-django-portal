from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.loginuser, name='loginuser'),
    url(r'^logout/', views.logout_user, name='logoutuser'),
    url(r'^validate/', views.get_token, name='validateCode'),
]