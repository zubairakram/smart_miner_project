from django.views.generic.base import View
from django.shortcuts import render

class Noise(View):
    template = 'noise.html'
    
    def get(self, request):
        return render(request, self.template, {})
    