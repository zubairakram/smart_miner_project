from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from smart_miner.forms import LoginForm
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def Login(request):
    form = LoginForm(request.POST or None)
    context = {
               'form' : form,
               'error': '',
    }
    return render(request, 'login.html', context)

def auth_view(request):
    form = LoginForm(request.POST or None)
    context = {
               'form' : form,
               'error': '',
    }
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            
            #return render(request, 'home.html', {})
            return HttpResponseRedirect('/home/')
        else:
            context['error'] = 'User is disabled'
            return render(request, 'login.html', context)
    else:
        context['error'] = "username/password is incorrect!"
        return render(request, 'login.html', context)
    
    
def Logout(request):
    logout(request)
    return render(request, 'logout.html', {})

@login_required
def home(request):
    return render(request, 'home.html', {})