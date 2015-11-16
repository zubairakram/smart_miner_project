from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from statistics import mean, mode

from smart_miner.forms import MissingForm
from smart_miner.views.loader import Loader


class Miner:
    """
    Abstract class for missing values algorithm containing class constructor
    and method to be overridden in child class.
    """
    def __init__(self, table):
        self.table = table
        
    def main(self):
        """
        main method uses helping methods and apply the algorithm in at data.
        """
        pass
    
    def transpose(self, table):
        """
        returns the transpose of the matrix.
        """
        output = []
        for item in range(len(table[0])):
            column = [row[item] for row in table]
            output.append(column)
        return output
    
    
class MeanImputation(Miner):
    """
    Mean Imputation algorithm for resolving missing values.
    """
    def __init__(self, table):
        Miner.__init__(self, table)
        
    def __calculate_value(self, row):
        """
        calculates mean or mode of the row according to situation
        """
        
        row = [item for item in row if not (item == "?" or item == "NULL" or item == "*")]
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
    
    def __impute_value(self, row):
        """
        imputes the missing values where require.
        """
        try:
            row = [int(item) for item in row]
        except:
            pass
        value = self.__calculate_value(row)
        
        out_put = []
        for i in row:
            if i == "*" or i == "?" or i == "NULL":
                out_put.append(value)
            else:
                out_put.append(i)

        return out_put
    
    
    def main(self):
        """
        Implements mean Imputation algorithm. by using helping functions
        first calculates missing values and then impute into the empty spaces.
        """         
        
        table = self.transpose(self.table)
        out_put = []
        
        for row in table:
            out_put.append(self.__impute_value(row))
        
        return self.transpose(out_put)        

class HotDeckImputation(Miner):
    """
    Implements Hot Deck Imputation algorithm to resolve missing values in the data-set.
    """
    def __init__(self, table):
        Miner.__init__(self, table)
    
    def __calculate_distance(self, m, n):
        """
        HOT DECK: calculates distance between two lists.
        """
        distance = 0
        size = len(m)
        for i in range(size):
            if m[i] != n[i] or n[i] in ('?', '*', 'NULL'):
                distance += 1
        return distance
    
    
    def __best_match(self, row, table):
        """
        HOT DECK: return the index of row having minimum distance with the respective row,
        """
        distances = []
        table_size = len(table)
        for i in range(table_size):
            if table.index(row) != i:  # ignores itself
                distance = self.__calculate_distance(row, table[i])
                distances.append((distance, i))
        return min(distances)[1]
    
    def __have_missing(self, row):
        """
        Return true is a row has missing value
        """
        if set(row) & set(("?", "*", "NULL")):
            return True
        else:
            return False
        
    def __impute_value(self, m, n):
        size = len(m)
        for i in range(size):
            if m[i] in ("*", "?", "NULL"):
                m[i] = n[i]
        return m
    
        
    def main(self):
        """
        impute values in the rows.
        """
        
        missing_indices = []  # record rows indices with missing index
        for row in self.table:
            if self.__have_missing(row):
                missing_indices.append(self.table.index(row))
        
        while missing_indices:
            for i in missing_indices:
                if not self.__have_missing(self.table[i]):
                    missing_indices.remove(i)
                else:
                    match = self.__best_match(self.table[i], self.table)
                    impute_row = self.__impute_value(self.table[i], self.table[match])
                    self.table[i] = impute_row
                    
        return self.table
    
    
    

class Missing(View):
    template = 'missing.html'
    form = MissingForm
    
    def __calculate_missings(self, table):
        """
        MEAN: calculate number of missing values in the data set.
        """
        counter = 0
        for row in table:
            for item in row:
                if item == "*" or item == '?' or item == "NULL":
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
            result = [table[0]]
            data = table[1:]
            if method == "1":
                myobject = MeanImputation(data)
            else:
                myobject = HotDeckImputation(data)
            data = myobject.main()
            for i in data:
                result.append(i)
            Loader.write_csv(result)
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
        ['Object ID', 'Name', 'Age', 'Sex', 'Blood Pressure', 'Cholesterol in mg/dl', 'Chest pain type', 'Defect type', 'Diagnosis'],
        ['1', 'Konrad Black', '31', 'male', '130', 'NULL', 'NULL', 'NULL', 'NULL'],
        ['2', 'Konrad Black', '31', 'male', '130', '331.2', '1', 'normal', 'absent'],
        ['3', 'Magda Doe', '26', 'female', '115', '407.5', '4', 'fixed', 'present'],
        ['4', 'Magda Doe', '26', 'female', '115', '407.5', '4', 'NULL', 'present'],
        ['5', 'Magda Doe', '26', 'female', '115', '407.5', 'NULL', 'NULL', 'NULL'],
        ['6', 'Magda Doe', '26', 'female', '115', '407.5', 'NULL', 'fixed', 'NULL'],
        ['7', 'Anna White', '56', 'female', '120', '45', '2', 'normal', 'absent'],
    ]
    for i in table:
        print(i)
    print("-"*120)
        
