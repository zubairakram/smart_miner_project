from django.shortcuts import render
from django.views.generic.base import View


class Missing(View):
    template = 'missing.html'
    
    def get(self, request):
        return render(request, self.template, {})
    
    def __mean_imputation(self):
        pass
    
    def __hot_deck_imputation(self):
        pass
    