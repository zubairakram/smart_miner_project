import csv

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from smart_miner.views.loader import read_csv


class Display(View):
    template = 'display.html'
    
    def get(self, request):
        try:
            table = read_csv()
            heading = table[0]
            data = table[1:]
            return render(request, self.template, {"heading": heading, "data": data})
        except:
            return render(request, self.template, {"alert": "no data exist to display"})

@login_required
def write_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=data.csv"
    writer = csv.writer(response)
    table = read_csv()
    for i in table:
        writer.writerow(i)
    return response
    
