from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from smart_miner.forms import LoginForm


class UserLogin(View):
    template = 'login.html'
    form = LoginForm
    context= {
                  'form': form,
                  'error': '',
    }
    
    def get(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if not request.user.is_authenticated():
            self.context['error'] = ''
            self.context['form'] = form
            return render(request, self.template, self.context)
        else:
            return HttpResponseRedirect('/upload/')
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        self.context['error'] = ''
        self.context['form'] = form
        
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                self.context['error'] = 'user is disabaled!'
                return render(request, self.template, self.context)
        else:
            self.context['error'] = "Invalid Username / Password Please re-enter!"
            return render(request, self.template, self.context)
    
            
class UserLogout(View):
    template = 'logout.html'
    
    def get(self, request):
        logout(request)
        return render(request, self.template, {})
