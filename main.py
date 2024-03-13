import Data_processing as pc
import Inserting_database as db
from visual import mapped_data,train_ideal 
'''
To compute the error and determine the  ideal function,
this method calls the necessary procedures and
finds the least amount of error by comparing it to the test data.
Additionally, it invokes a procedure that plots all of these mistakes, 
the ideal function, and data mapping.
'''
def load_dataframes(file_test, file_train, file_ideal):
    testdf = pc.optimal_function_operation(file_test)
    traindf = pc.optimal_function_operation(file_train)
    idealdf = pc.Data_Input_Processing(file_ideal)
    return testdf, traindf, idealdf

def compute_ideal_function(traindf, idealdf):
    pc.optimal_Function(traindf, idealdf)
    return traindf.ideal_DataIndex(), traindf.ideal_MaxError()

def process_test_data(testdf, idealdf, idealDataIndices, idealDataErrors):
    return pc.ideal_error_test_information(testdf, idealdf, idealDataIndices, idealDataErrors)

def mainFunction():
    testdf, traindf, idealdf = load_dataframes("inputData/test.csv", "inputData/train.csv", "inputData/ideal.csv")

    idealDataIndices, idealDataErrors = compute_ideal_function(traindf, idealdf)

    map_data, small_err = process_test_data(testdf, idealdf, idealDataIndices, idealDataErrors)

    db.database_insertion(traindf, testdf, idealdf, map_data, small_err, idealDataIndices)
    indices = [1, 2, 3, 4]

# Create blank lists at first to store the results.
    x_values_list = []
    y_values_list = []

# Loop through indices and extract test data
    for val in indices:
       x_values, y_values = pc.test_data_extraction(map_data, testdf, val)
       x_values_list.append(x_values)
       y_values_list.append(y_values)

# Iterate through the indexes and retrieve test data
    (x_values1, y_values1), (x_values2, y_values2), (x_values3, y_values3), (x_values4, y_values4) = zip(x_values_list, y_values_list)
    train_ideal(traindf, idealdf, idealDataIndices)
# Singular function calls
    mapped_data(idealdf, idealDataErrors, idealDataIndices, x_values1, y_values1, 1)
    mapped_data(idealdf, idealDataErrors, idealDataIndices, x_values2, y_values2, 2)
    mapped_data(idealdf, idealDataErrors, idealDataIndices, x_values3, y_values3, 3)
    mapped_data(idealdf, idealDataErrors, idealDataIndices, x_values4, y_values4, 4)

if __name__ == '__main__':
    mainFunction()
