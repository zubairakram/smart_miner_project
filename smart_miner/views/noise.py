from django.shortcuts import render
from django.views.generic.base import View


class Noise(View):
    template = 'noise.html'
    
    def get(self, request):
        return render(request, self.template, {})
    
    def post(self):
        pass
    