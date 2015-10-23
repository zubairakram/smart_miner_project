import csv

from django.shortcuts import render
from django.views.generic.base import View

from final_project.settings import MEDIA_ROOT
from smart_miner.forms import UploadForm
from django.db import models


class Loader(View):
    """
    This class contains method for collecting data from file and parse the data.
    and the save the data in data base.
    """
    template = "upload.html"
    form = UploadForm
    context = {
               "form": form,
               "error": '',
               "success": '',
               }
    
    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            self.__process_file(request.FILES['file'])
            self.context['success']= "uploaded successfully!"
            self.context['form'] = form
            return render(request, self.template, self.context)
        else:
            self.context['error']= "cannot upload the file!"
            return render(request, self.template, self.context)

    def get(self, request):            
            return render(request, self.template, self.context)

    def __process_file(self, file):
        with open(MEDIA_ROOT + 'data.csv', 'wb+') as fout:
            for i in file.chunks():
                fout.write(i)
    
    
    def create_table(self):
        """
        This method takes first line of the CSV file parse it and find out the
        data type of each column. according to these data type return a dictionary
        of the Table columns to be created in the Model
        {'column_name': fieldType()}
        """
        with open(self.file) as fin:        # creates file object
            matrix = list(csv.reader(fin))
            number_of_columns = len(matrix[0])
            
        attrs = {"__module__": "smart_miner.models"} # Virtual Model attributes
        
        i = 0
        while i < number_of_columns:
            column = matrix[0][i]
            try:
                column = int(column)
                attrs["col{}".format(column)] = models.IntegerField()
            except:
                attrs["col{}".format(column)] = models.CharField(max_length=32)
            i += 1
        return attrs

 
if __name__ == '__main__':
    data = Loader(MEDIA_ROOT+'data.csv')
    
    d = data.create_table()
    for k, v in d.items():
        print(k,"\t\t", v)
     
