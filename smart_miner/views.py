from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from smart_miner.forms import LoginForm, UploadForm


def Login(request):
    form = LoginForm(request.POST or None)
    context = {
               'form' : form,
               'error': '',
    }
    
    # if method is POST 
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                context['error'] = 'User is disabled'
                return render(request, 'login.html', context)
        else:
            context['error'] = "Invalid Username / Password Please re-enter!"
            return render(request, 'login.html', context)
    
    # if method is GET
    else:
        if not request.user.is_authenticated():
            return render(request, 'login.html', context)
        else:
            return HttpResponseRedirect('/upload/')
        

    
def Logout(request):
    logout(request)
    return render(request, 'logout.html', {})

@login_required
def upload_data(request):
    form = UploadForm(request.POST or None)
    context = {"form": form}
    return render(request, 'upload.html', context)

@login_required
def classify_data(request):
    return render(request, 'classify.html', {})

@login_required
def missing_values(request):
    return render(request, 'missing.html', {})

@login_required
def remove_noise(request):
    return render(request, 'noise.html', {})

@login_required
def generate_report(request):
    return render(request, 'report.html', {})




