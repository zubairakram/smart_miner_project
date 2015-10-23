from django.shortcuts import render
from django.views.generic.base import View


class Report(View):
    template = 'report.html'
    
    def get(self, request):
        return render(request, self.template, {})
    