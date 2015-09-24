from django.conf.urls import url

from smart_miner import views


urlpatterns = [
    url(r'login/$', views.login, name='login'),
    url(r'hello/$', views.hello , name='hello'),
]