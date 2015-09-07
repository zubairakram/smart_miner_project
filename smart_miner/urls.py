from django.conf.urls import url
from smart_miner.views import index

urlpatterns = [
    url(r'$', index),
]