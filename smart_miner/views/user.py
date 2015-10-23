from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from smart_miner.forms import LoginForm


class UserLogin(View):
    form = LoginForm
    template = "login.html"
    context = {
               'form': form,
               'error': '',
    }

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render(request, self.template, self.context)
        else:
            return HttpResponseRedirect('/upload/')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                self.context['error'] = 'User is disabled'
                return render(request, self.template, self.context)
        else:
            self.context['error'] = "Invalid Username / Password Please re-enter!"
            return render(request, 'login.html', self.context)
    
            
class UserLogout(View):
    template = 'logout.html'
    
    def get(self, request):
        logout(request)
        return render(request, self.template, {})
