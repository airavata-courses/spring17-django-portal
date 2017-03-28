from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.tab2, name='tab2'),
]