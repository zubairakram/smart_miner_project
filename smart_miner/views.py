from django.shortcuts import render

from smart_miner.forms import LoginForm


def login(request):
    form = LoginForm(request.POST or None)
    
    context = {
               'form' : form,
               'error': 'Invalid username/password please re-enter',
    }
    
    return render(request, 'login.html', context)
    
    
def hello(request):
    return render(request, 'hello.html', {"name": "Zubair"})

def form(request):
    form = LoginForm(request.POST or None)
    
    context = {'form': form}
    return render(request, 'form.html', context)
