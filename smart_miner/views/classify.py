from django.shortcuts import render
from django.views.generic.base import View

from smart_miner.views.loader import Loader
from smart_miner.views.missing import Miner


class OneR(Miner):
    """
    OneR algorithm use
    """
    def __init__(self, table):
        Miner.__init__(self, table)
        
        
    def frequency_string(self, predictor='Outlook'):
        """
        calculates the frequencies of each indicator having string values of
        the given predictors values of indicators are given in string.
        and gives the output in the form of following:
            {    
            indicator: [yes, no],
            ...
        }
        """
        predictor_index = self.table[0].index(predictor)
        indicators = {}
        data = self.table[1:]
        for row in data:
            indicator = row[predictor_index]
            if row[predictor_index] in indicators:
                pass
            else:
                indicators[indicator] = [0, 0]
            if row[-1] == 'Yes':
                indicators[indicator][0] += 1
            else:
                indicators[indicator][1] += 1
        return indicators
    
    def frequency_numeric(self, predictor='Temperature'):
        """
        calculates the frequencies of each indicator having numeric values of
        the given predictors values of indicators are given in string.
        and gives the output in the form of following:
            {    
            indicator: [yes, no],
            ...
        }
        """
        predictor_index = self.table[0].index(predictor)
        indicators = {}
        data = self.table[1:]
        column = sorted([int(row[predictor_index]) for row in data])
        column_size = len(column)
        a = column[round(column_size / 3)]  # 1st class limit
        b = column[round((column_size / 3) * 2)]  # 2nd class limit
        
        class1 = "<= {}".format(a)
        class2 = "> {} and <= {}".format(a, b)
        class3 = "> {}".format(b)
        
        # initiating values for each indicator
        indicators[class1] = [0, 0]
        indicators[class2] = [0, 0]
        indicators[class3] = [0, 0]
        
        for row in data:
            indicator = int(row[predictor_index])
            if indicator <= a:
                if row[-1] == "Yes":
                    indicators[class1][0] += 1
                else:
                    indicators[class1][1] += 1
            elif a < indicator <= b:
                if row[-1] == "Yes":
                    indicators[class2][0] += 1
                else:
                    indicators[class2][1] += 1
            else:  # if indicator fall in 3rd class
                if row[-1] == "yes":
                    indicators[class3][0] += 1
                else:
                    indicators[class3][0] += 1
        return indicators
    
    def calculate_frequency_table(self):
        """
        calculate frequency and return a frequency table of the given data set
        in the following form
        OUTPUT
        frequency_table = {
            predictor: {
                indicator : [yes, no],
                ...
            }
            ...
        }
        """
        predictors = self.table[0]
        frequency_table = {}
        for predictor in predictors[:-1]:
            predictor_index = predictors.index(predictor)
            try:
                float(self.table[1][predictor_index])
                frequency_table[predictor] = self.frequency_numeric(predictor)
            except:
                frequency_table[predictor] = self.frequency_string(predictor)
                
        return frequency_table


    def calculate_error(self, predictor):
        """
        helping function use in choose_predictor function:
        get input in the form of following data structure.
        predictor: {
                    indicator1: [yes, no],
                    indicator2: [yes, no],
                    ...
                    }
        calculates total error of the predictor
        return value is in the form of integer.
        """
        error = 0
        for i in predictor:
            indicator = predictor[i]  # get the value of indicator
            if indicator[0] < indicator[1]:
                error += indicator[0]
            else:
                error += indicator[1]
        return error
  
    def choose_predictor(self):
        """
        calculate error rate of each predictor and record in predictors list
        in the following form:
        
        [(error_rate, predictor),...]
        
        choose predictor from frequency table with minimum error rate.
        """
        frequency_table = self.calculate_frequency_table()
        predictors = []  # list of predictors with error rate
        for predictor in frequency_table:  # calculate error of each predictor
            error = self.calculate_error(frequency_table[predictor])
            predictors.append((error, predictor))
        return min(predictors)
    
    def main(self):
        predictor = self.choose_predictor()[1]
        frequency_table = self.calculate_frequency_table()[predictor]
        result = self.table[0][-1]
        message = []
        for indicator, v in frequency_table.items():
            yes_no = ''
            if v[0] > v[1]:
                yes_no = 'Yes'
            else:
                yes_no = 'No'
                
            line = "IF {predictor} is {indicator} THEN {result} = {yes_no}".format(
                                                    predictor=predictor,
                                                    indicator=indicator,
                                                    result=result,
                                                    yes_no=yes_no
                                                )
            message.append(line)
        return message


class Classify(View):
    template = 'classify.html'
        
    def get(self, request):
        return render(request, self.template, {})
    
    def post(self, request):
        table = Loader.read_csv()
        myobject = OneR(table)
        print(myobject.main())
        context = {'message': myobject.main()}
        return render(request, self.template, context)
    


# unit tests
if __name__ == '__main__':
    table2 = [
            ['Outlook', 'Temperature', 'Humidity', 'Windy', 'Play'],
            ['Sunny', 'Hot', 'High', 'FALSE', 'No'],
            ['Sunny', 'Hot' , 'High' , 'TRUE', 'No'],
            ['Overcast' , 'Hot'  , 'High', 'FALSE', 'Yes'],
            ['Rainy', 'Mild', 'High', 'FALSE', 'Yes'],
            ['Rainy', 'Cool', 'Normal', 'FALSE', 'Yes'],
            ['Rainy', 'Cool', 'Normal', 'TRUE', 'No'],
            ['Overcast', 'Cool', 'Normal', 'TRUE', 'Yes'],
            ['Sunny', 'Mild', 'High', 'FALSE', 'No'],
            ['Sunny', 'Cool', 'Normal', 'FALSE', 'Yes'],
            ['Rainy', 'Mild', 'Normal', 'FALSE', 'Yes'],
            ['Sunny', 'Mild', 'Normal', 'TRUE', 'Yes'],
            ['Overcast', 'Mild', 'High', 'TRUE', 'Yes'],
            ['Overcast', 'Hot', 'Normal', 'FALSE', 'Yes'],
            ['Rainy', 'Mild', 'High', 'TRUE', 'No']
    ]

    
    table = [
        ['Outlook', 'Temperature', 'Humidity', 'Windy', 'Play'],
        ['Sunny', '65', '60', 'FALSE', 'No'],
        ['Sunny', '64', '63', 'TRUE', 'No'],
        ['Overcast ', '68', '66', 'FALSE', 'Yes'],
        ['Rainy', '69', '69', 'FALSE', 'Yes'],
        ['Rainy', '70', '72', 'FALSE', 'Yes'],
        ['Rainy', '71', '75', 'TRUE', 'No'],
        ['Overcast', '72', '78', 'TRUE', 'Yes'],
        ['Sunny', '72', '81', 'FALSE', 'No'],
        ['Sunny', '75', '84', 'FALSE', 'Yes'],
        ['Rainy', '75', '87', 'FALSE', 'Yes'],
        ['Sunny', '80', '90', 'TRUE', 'Yes'],
        ['Overcast', '81', '93', 'TRUE', 'Yes'],
        ['Overcast', '83', '96', 'FALSE', 'Yes'],
        ['Rainy', '85', '100', 'TRUE', 'No']
    ]
    
    frequency_table = {
            'Humidity': {
                'Normal': [6, 1],
                'High': [3, 4]
            },
                       
            'Temperature': {
                'Mild': [4, 2],
                'Cool': [3, 1],
                'Hot': [2, 2]
            },
                       
            'Outlook': {
                'Rainy': [3, 2],
                'Overcast': [4, 0],
                'Sunny': [2, 3]
            },
                       
            'Windy': {
                'TRUE': [3, 3],
                'FALSE': [6, 2]
            }
                       
    }
    
    table = Loader.read_csv()
    myobject = OneR(table)
    result = myobject.calculate_frequency_table()
    for k,v in result.items():
        print(k,v)
