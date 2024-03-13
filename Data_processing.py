import numpy as np


class Data_Input_Processing(object):
    def __init__(self, filename):
        try:
            self.file = open(filename, "rb")
            self.inputData = np.genfromtxt(self.file, delimiter=",", skip_header=1)
           
            self.x_data = self.inputData[:, 0]
           
            self.rows = self.inputData.shape[0]
            self.cols = self.inputData.shape[1]
            self.file.close()

        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.filename}")
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

    def rx_data(self):
        if self.x_data is not None:
            return self.x_data  
        else:
            raise ValueError("No x data available. Please read the file first.")

  
    def ry_data(self, i=1):
        try:
            column_index = int(i) 
            if not 0 <= column_index < self.cols:
                raise IndexError(f"Invalid column index: {column_index}") 
            return self.inputData[:, column_index]
        except ValueError:
            raise IndexError("Invalid column index. Please provide a valid integer.")
        except IndexError as e:
            raise IndexError(f"Error accessing y data: {e}")

    def rrows(self):
        return self.rows

    def rcols(self):
        return self.cols
     
    def xy_cell_data(self, row, column):
        try:
            if 0 <= row < self.rows and 0 <= column < self.cols:
                return self.inputData[row, column]
            else:
                raise IndexError("Invalid row or column index")
        except IndexError as e:
            raise IndexError(f"Error accessing cell data: {e}")



class optimal_function_operation(Data_Input_Processing):
    def __init__(self, filename):
        Data_Input_Processing.__init__(self, filename)
        self.assignedIdealFunc = []
        self.errorSum = []
        self.maxError = []

    def assignIdealFunction(self, ideal_func_index, error_sum, max_err):
        self.assignedIdealFunc += [ideal_func_index]
        self.errorSum += [error_sum]
        self.maxError += [max_err]

    def ideal_DataIndex(self):
        return self.assignedIdealFunc

    def ideal_SumError(self):
        return self.errorSum

    def ideal_MaxError(self):
        return self.maxError

def optimal_Function(train_df, ideal_df):
    totalErrorTemp = 0.0
    totalError = None
    maximumError = 0
    indexIdeal = None
    for col_tr in range(1, train_df.rcols()):
        for col_id in range(1, ideal_df.rcols()):
            for row_id in range(0, ideal_df.rrows()):
                totalErrorTemp = totalErrorTemp + (ideal_df.xy_cell_data(row_id, col_id) -
                                                    train_df.xy_cell_data(row_id, col_tr)) ** 2
            if (totalError is None) or (totalErrorTemp <= totalError):
                totalError = totalErrorTemp
                indexIdeal = col_id
            else:
                pass
            totalErrorTemp = 0
        for m in range(0, ideal_df.rows):
            maximumErrorTemp = ideal_df.xy_cell_data(m, indexIdeal) - train_df.xy_cell_data(m, col_tr)
            if (maximumError is None) or (maximumErrorTemp > maximumError):
                maximumError = maximumErrorTemp
            else:
                pass
        train_df.assignIdealFunction(indexIdeal, totalError, maximumError)
        totalError = None
        maximumError = 0
        indexIdeal = None

def ideal_error_test_information(testing_data, ideal_set_values, ideal_data_index, ideal_data_errors):
    map_fun = []
    map_err = []
    var = None
    low_err = 0
    for row_t in range(0, testing_data.rrows()):
        for row_id in range(0, ideal_set_values.rrows()):
            if testing_data.xy_cell_data(row_t, 0) == ideal_set_values.xy_cell_data(row_id, 0):
                for i in range(0, len(ideal_data_index)):
                    temporary_err = abs(ideal_set_values.xy_cell_data(row_id, ideal_data_index[i]) -
                                        testing_data.xy_cell_data(row_t, 1))
                    if i == 0:
                        low_err = temporary_err
                    if low_err <= (ideal_data_errors[i] * np.sqrt(2)):
                        var = i
                    elif (i != 0) and (temporary_err < low_err):
                        low_err = temporary_err
                if low_err <= (ideal_data_errors[i] * np.sqrt(2)):
                    var = i
                map_fun.append(var)
                map_err.append(low_err)
                var = None
                low_err = 0
    return map_fun, map_err

def test_data_extraction(mapp, test, select_data):
    
    val_x4 = []
    val_y4 = []
    val_x3 = []
    val_y3 = []
    val_x2 = []
    val_y2 = []
    val_x1 = []
    val_y1 = []
    val_x = []
    val_y = []      
    ideal_fun_dict = {0: [], 1: [], 2: [], 3: [], 'other': []}
    for k, value in enumerate(mapp):
        if value in ideal_fun_dict:
            ideal_fun_dict[value].append(k) 
        else:
            ideal_fun_dict['other'].append(k)

    ideal_fun1 = ideal_fun_dict.get(0, [])
    ideal_fun2 = ideal_fun_dict.get(1, [])
    ideal_fun3 = ideal_fun_dict.get(2, [])
    ideal_fun4 = ideal_fun_dict.get(3, [])
    ideal_same = ideal_fun_dict.get('other', [])
    val_x4 = [test.xy_cell_data(k, 0) for k in ideal_fun4]
    val_y4 = [test.xy_cell_data(k, 1) for k in ideal_fun4]
    val_x3 = [test.xy_cell_data(k, 0) for k in ideal_fun3]
    val_y3 = [test.xy_cell_data(k, 1) for k in ideal_fun3]
    val_x2 = [test.xy_cell_data(k, 0) for k in ideal_fun2]
    val_y2 = [test.xy_cell_data(k, 1) for k in ideal_fun2]
    val_x1 = [test.xy_cell_data(k, 0) for k in ideal_fun1]
    val_y1 = [test.xy_cell_data(k, 1) for k in ideal_fun1]
    val_x = [test.xy_cell_data(k, 0) for k in ideal_same]
    val_y = [test.xy_cell_data(k, 1) for k in ideal_same]
 
    data_mapping = {
    4: (val_x4, val_y4),
    3: (val_x3, val_y3),
    2: (val_x2, val_y2),
    1: (val_x1, val_y1),
    "None": (val_x, val_y)
    }

    return data_mapping.get(select_data, (val_x, val_y))


def squaredError(train_df, ideal_df):
    squared_errors = (ideal_df["y"].values - train_df["y"].values) ** 2
    deviationTotal = np.sum(squared_errors)
    return deviationTotal