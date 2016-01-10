from django.shortcuts import render
from django.views.generic.base import View
import statistics

from smart_miner.views.loader import Loader
from smart_miner.views.missing import Miner


class Binning(Miner):
    """
    binning algorithm implementation used to remove noise from data set.
    """
    
    def __init__(self, table):
        Miner.__init__(self, table)
    
    def calculate_bin(self, row, min_value, max_value):
        """
        calculate bins and return a corrected row
        """
        row = [float(i) for i in row]
        if max(row) > max_value or min(row) < min_value:
            row_size = len(row)
            sorted_row = sorted(list(set(row)))
            bin_size = int(row_size / 2)
            bin1 = sorted_row[:bin_size]
            bin1_mean = statistics.mean(bin1)
            
            bin2 = sorted_row[bin_size:]
            bin2_mean = statistics.mean(bin2)
                    
            for item in row:
                item_index = row.index(item)
                if bin1[0] <= item <= bin1[-1]:
                    row[item_index] = round(bin1_mean, 1)
                else:
                    row[item_index] = round(bin2_mean, 1)
            return row
        else:
            return row

    
    def get_max_min(self, request_post):
        """
        converts the request.POST data to standard python dictionary
        and make it use able.
        example: 
        request_post = {
            'Age_min': ['20'],
            'Age_max': ['60'],
    
            'Blood Pressure_min': ['110'],
            'Blood Pressure_max': ['140'],
    
            'Cholesterol in mg/dl_min': ['50'],
            'Cholesterol in mg/dl_max': ['600'],
    
            'Chest pain type_min': ['1'],
            'Chest pain type_max': ['5'],
            
            'csrfmiddlewaretoken': ['blabla']
        }
        """
        fields = {}
        for k, v in request_post.items():
            field = k[:-4]
            if field in fields or field.startswith('csrf'):
                continue
            else:
                fields[field] = [0, 0]
        
        for k, v in request_post.items(): 
            item = k[:-4]
            if k.startswith('csrf'):
                continue
            elif k.endswith('_min'):
                fields[item][0] = float(v[0])
            else:
                fields[item][1] = float(v[0])
        return fields
    
    def main(self, request_post):
        '''
        main implementation of binning algorithm on the data set.
        '''
        heading = self.table[0]
        data = self.transpose(self.table[1:])
        
        fields = self.get_max_min(request_post)
        
        for k, v in fields.items():
            index = heading.index(k)
            min_value = v[0]
            max_value = v[1]
            data[index] = self.calculate_bin(data[index], min_value, max_value)
        
        result = []
        result.append(heading)
        for i in self.transpose(data):
            result.append(i)
        return result

# django view class use Binning algo for removing noise.

class Noise(View):
    template = 'noise.html'
    
    def get(self, request):
        table = Loader.read_csv()
        for row in table:
            for item in row:
                if item in ('NULL', '*', '?'):
                    message = "there are missing values in your data, fill them first."
                    return render(request, self.template, {'message': message})
            
        row_size = len(table[0])
        fields = []
        for i in range(1, row_size):
            try:
                float(table[1][i])
                fields.append(table[0][i])
            except:
                pass
        return render(request, self.template, {"fields": fields})
    
    def post(self, request):
        request_post = dict(request.POST)
        table = Loader.read_csv()
        myobject = Binning(table)
        result = myobject.main(request_post)
        Loader.write_csv(result)
        
        context = {'success': 'Operation completed Successfully!'}
        return render(request, self.template, context)


# unit tests
if __name__ == '__main__':
    table = [
        ['Object ID', 'Name', 'Age', 'Sex', 'Blood Pressure', 'Cholesterol in mg/dl', 'Chest pain type', 'Defect type', 'Diagnosis'],
        ['1', 'Konrad Black', '31', 'male', '130', '261.2', '2.3', 'normal', 'absent'],
        ['2', 'Konrad Black', '31', 'male', '130', '331.2', '1', 'normal', 'absent'],
        ['3', 'Magda Doe', '26', 'female', '115', '261.2', '4', 'fixed', 'present'],
        ['4', 'Magda Doe', '26', 'female', '115', '407.5', '2.3', 'normal', 'absent'],
        ['5', 'Anna White', '56', 'female', '120', '45', '2', 'normal', 'absent']
    ]
    
    transposed = [
        ['1', '2', '3', '4', '5'],
        ['Konrad Black', 'Konrad Black', 'Magda Doe', 'Magda Doe', 'Anna White'],
        ['31', '31', '26', '26', '56'],
        ['male', 'male', 'female', 'female', 'female'],
        ['130', '130', '115', '115', '120'],
        ['261.2', '331.2', '261.2', '407.5', '45'],
        ['2.3', '1', '4', '2.3', '2'],
        ['normal', 'normal', 'fixed', 'normal', 'normal'],
        ['absent', 'absent', 'present', 'absent', 'absent']
    ]
    

    
#     row = [float(i) for i in transposed[4]]
#     print(calculate_bin(row, 110, 140))
    
    
    
    
    d = {
        'Age_min': 20,
        'Age_max': 60,
        
        'Blood Pressure_min': 110,
        'Blood Pressure_max': 140,
        
        'Cholesterol in mg/dl_min': 50,
        'Cholesterol in mg/dl_max': 600,
        
        'Chest pain type_min': 1,
        'Chest pain type_man': 5,
    }
    
    request_post = {        # request post kwargs
        'Age_min': ['20'],
        'Age_max': ['60'],

        'Blood Pressure_min': ['110'],
        'Blood Pressure_max': ['140'],

        'Cholesterol in mg/dl_min': ['50'],
        'Cholesterol in mg/dl_max': ['600'],

        'Chest pain type_min': ['1'],
        'Chest pain type_max': ['5'],
        
        'csrfmiddlewaretoken': ['blabla']
    }
    