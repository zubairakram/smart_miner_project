from django.views.generic.base import View
from django.shortcuts import render

class Missing(View):
    template = 'missing.html'
    
    def get(self, request):
        return render(request, self.template, {})
    