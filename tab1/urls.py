from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tab1, name='tab1'),
]