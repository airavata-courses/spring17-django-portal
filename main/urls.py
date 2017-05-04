from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^main$', views.main, name='main'),
    url(r'^test/$',views.test_api),
    url(r'^login$',views.login_view,name='login_view'),
    url(r'^login/auth$', views.login_api, name='login'),
    url(r'^create/user$',views.create_user_view,name='create_user_view'),
    url(r'^api/create/user$',views.create_user,name='create_user'),

]