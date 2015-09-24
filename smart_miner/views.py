from django.shortcuts import render
from django.contrib.auth import authenticate



def login(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render(request, 'login.html',{'state':state, 'username': username})


def hello(request):
    
    return render(request, 'hello.html', {"name": "Zubair"})
