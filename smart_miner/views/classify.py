from django.shortcuts import render
from django.views.generic.base import View
from smart_miner.views.missing import Miner


class OneR(Miner):
    pass

class Classify(View):
    template = 'classify.html'
        
    def get(self, request):
        return render(request, self.template, {})
    
    def post(self, request):
        return render(request, self.template, {})
    

if __name__ == '__main__':
    table_one = [
        ['Outlook', 'Temperature', 'Humidity', 'Windy', 'Play golf'],
        ['Rainy', 'Hot', 'High', 'FALSE', 'No'],
        ['Rainy', 'Hot', 'High', 'TRUE', 'No'],
        ['Overcast', 'Hot', 'High', 'FALSE', 'Yes'],
        ['Sunny', 'Mild', 'High', 'FALSE', 'Yes'],
        ['Sunny', 'Cool', 'Normal', 'FALSE', 'Yes'],
        ['Sunny', 'Cool', 'Normal', 'TRUE', 'No'],
        ['Overcast', 'Cool', 'Normal', 'TRUE', 'Yes'],
        ['Rainy', 'Mild', 'High', 'FALSE', 'No'],
        ['Rainy', 'Cool', 'Normal', 'FALSE', 'Yes'],
        ['Sunny', 'Mild', 'Normal', 'FALSE', 'Yes'],
        ['Rainy', 'Mild', 'Normal', 'TRUE', 'Yes'],
        ['Overcast', 'Mild', 'High', 'TRUE', 'Yes'],
        ['Overcast', 'Hot', 'Normal', 'FALSE', 'Yes'],
        ['Sunny', 'Mild', 'High', 'TRUE', 'No']
    ]
    
    
    def calculate_frequency(table):
        """
        Create frequency table of the given data set.
        """
        row_size = len(table[0])
        frequency_table = {}
        i = 0
        while i < (row_size - 1):
            predictor = table[0][i]
            if predictor in frequency_table:
                pass
            else:
                frequency_table[predictor] = {}
            for row in table[1:]:
                item = row[i]
                if item in frequency_table[predictor]:
                    pass
                else:
                    frequency_table[predictor][item] = [0, 0]
                if row[-1] == "Yes":
                    frequency_table[predictor][item][0] += 1
                else:
                    frequency_table[predictor][item][1] += 1
            i += 1
        return frequency_table
    
    table = {
            'Windy': {
                    'FALSE': [6, 2],
                    'TRUE': [3, 3]
                    },
             
            'Temperature': {
                    'Mild': [4, 2],
                    'Hot': [2, 2],
                    'Cool': [3, 1]
                    },
             
            'Humidity': {
                    'Normal': [6, 1],
                    'High': [3, 4]
                    },
            'Outlook': {
                    'Rainy': [2, 3],
                    'Sunny': [3, 2],
                    'Overcast': [4, 0]
                    }
            }

    d = table['Windy']
    def calculate_error(d):
        """
        calculates error of a class of a predictor
        """
        error = 0
        for i in d:
            item = d[i]
            if item[0] < item[1]:
                error += item[0]
            else:
                error += item[1]
        return error
    
#     print(calculate_error(d))

    def total_error(table):
        """
        calculates the total error from frequency table
        and return the class with minimum error.
        """
        error_rate = []
        for predictor in table:
            error = calculate_error(table[predictor])
            error_rate.append((error, predictor))
        return error_rate
    
    result = total_error(table)
    print(min(result))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
