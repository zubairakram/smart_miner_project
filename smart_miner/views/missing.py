from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from statistics import mean, mode

from smart_miner.forms import MissingForm
from smart_miner.views.loader import Loader


class Missing(View):
    template = 'missing.html'
    form = MissingForm
    
    ############ Mean imputation helping functions ##################
    def calculate_value(self, row):
        """
        Mean Imputation helping function
        """
        row = [item for item in row if not (item == "" or item == "NULL" or item == 0)]
        print(row)
        value = ""
        try:
            row = [float(i) for i in row]
            value = round(mean(row), 1)
        except:
            try:
                value = mode(row)
            except:
                value = row[0]
        return value
    
    def transpose(self, table):
        output = []
        for item in range(len(table[0])):
            column = [row[item] for row in table]
            output.append(column)
        return output
    
    def impute_value(self, row):
        try:
            row = [int(item) for item in row]
        except:
            pass
        value = self.calculate_value(row)
        
        out_put = []
        for i in row:
            if i == 0 or i == "" or i == "NULL":
                out_put.append(value)
            else:
                out_put.append(i)

        return out_put
    
        
    def mean_imputation(self, table):
        header = table[0]
        data = table[1:]
        
        data = self.transpose(data)
        out_put = []
        
        for row in data:
            out_put.append(self.impute_value(row))
        
        out_put = self.transpose(out_put)
        print(header)
        result = []
        result.append(header)
        for i in out_put:
            result.append(i)    
        print(result)
        Loader.write_csv(result)
    
    def hot_deck_imputation(self):
        pass
    

    def __calculate_missings(self, table):
        """
        calculate number of missing values in the data set.
        """
        counter = 0
        for row in table:
            for item in row:
                if item == "" or item == '0' or item == "NULL":
                    counter += 1
        
        return counter 
    
    
    def get(self, request):
        "every time read data from directory"
        table = Loader.read_csv()[1:]
        total_missings = self.__calculate_missings(table)
        if total_missings:
            context = {
                       'form': self.form,
                       'info': '"{}" values missing in your data'.format(total_missings)
            }
        else:
            context = {
                       "form": self.form,
                       'message': "No missing values found in the data."
            }
            
        return render(request, self.template, context)
    
    def post(self, request):
        "every time read data from directory"
        form = self.form(request.POST or None)
        method = request.POST.get('method', '')
        table = Loader.read_csv()
        if form.is_valid():
            if method == "1":
                self.mean_imputation(table)
                return HttpResponseRedirect("/missing/")
            else:
                self.hot_deck_imputation()
                return HttpResponseRedirect("/missing/")
        else:
            context = {
                       'form': form,
                       'error': 'Select one method before action!'
            }
            return render(request, self.template, context)
        


# unit tests
if __name__ == '__main__':
    table = [
        ['zubair',  'akram',    '334',  'jhang',    'pakistan', '36508'],
        ['uzair',   '',         '335',  'fsd',      '',         '12345'],
        ['umair',   'akram',    '0',  '',         'pakistan', '67890'],
        ['hamid',   'hameed',   '300',  'Null',      'usa',      '23245'],
        ['ahmad',   'ahsan',    '364',  'jhang',      'pakistan', '76543'],
    ]
    
    table2 = [
        ['zubair', 'uzair', 'umair', 'hamid', 'ahmad'],
        ['akram', '', 'akram', 'hameed', 'ahsan'],
        ['334', '335', '0', '300', '364'],
        ['jhang', 'fsd', '', 'grw', 'jhang'],
        ['pakistan', '', 'pakistan', 'usa', 'pakistan'],
        ['36508', '12345', '67890', '23245', '76543']
    ]
     
#     def calculate_value(row):
#         row = [item for item in row if not (item == "" or item == "NULL" or item == 0)]
#         value = ""
#         try:
#             row = [int(i) for i in row]
#             value = mean(row)
#         except:
#             try:
#                 value = mode(row)
#             except:
#                 value = row[0]
#         return value
#     
#     def transpose(table):
#         output = []
#         for item in range(len(table[0])):
#             column = [row[item] for row in table]
#             output.append(column)
#         return output
#     
#     def impute_value(row):
#         try:
#             row = [int(item) for item in row]
#         except:
#             pass
#         value = calculate_value(row)
#         
#         out_put = []
#         for i in row:
#             if i == 0 or i == "" or i == "NULL":
#                 out_put.append(value)
#             else:
#                 out_put.append(i)
# 
#         return out_put
#     
#         
#     def mean_imputation(table):
#         table = transpose(table)
#         out_put = []
#         for row in table:
#             out_put.append(impute_value(row))
#             
#         return transpose(out_put)
#     
# 
#     for row in table:
#         for item in row:
#             print(item, '\t\t\t', end="")
#         print()
#     print()
#  
#     for row in mean_imputation(table):
#         for item in row:
#             print(item, '\t\t\t', end="")
#         print()
 
#       
# #     print(out_put)
# #     for row in table:
# #         for col in row: 
# #             print(col)
# #         
#  