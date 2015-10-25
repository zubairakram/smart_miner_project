from django.shortcuts import render
from django.views.generic.base import View
from smart_miner.views.loader import read_csv

class Miner(View):
    table = read_csv()
    
    def hello(self):
        print("hello world")
        
class Classify(Miner):
    template = 'classify.html'
    
    
    def get(self, request):
        return render(request, self.template, {})
    
    def post(self, request):
        return render(request, self.template, {})
    
    def one_r(self):
        print(self.table)
        

if __name__ == '__main__':
    c = Classify()
    c.hello()