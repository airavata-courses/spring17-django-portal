from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.home,name="home"),
    url(r'^key/generate$',view=views.generate_ssh,name="key-gen"),
    url(r'^gateway/register',views.register_gatway,name="gateway-registration"),

]