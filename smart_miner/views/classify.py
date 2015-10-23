from django.shortcuts import render
from django.views.generic.base import View


class Classify(View):
    template = 'classify.html'
    
    def get(self, request):
        return render(request, self.template, {})
    