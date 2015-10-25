"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from smart_miner.views import user, classify, missing, loader, noise, display


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', user.UserLogin.as_view(), name='login'),
    url(r'^logout/$', user.UserLogout.as_view(), name='logout'),
    url(r'^upload/$', login_required(loader.Loader.as_view()), name='upload'),
    url(r'^classify/$', login_required(classify.Classify.as_view()), name='classify'),
    url(r'^missing/$', login_required(missing.Missing.as_view()), name='missing'),
    url(r'^noise/$', login_required(noise.Noise.as_view()), name='noise'),
    url(r'^display/$', login_required(display.Display.as_view()), name='display'),
    url(r'^csv/$', display.write_csv, name="csv"),
]
