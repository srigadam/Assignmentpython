import numpy as np
import matplotlib.pyplot as plt

''' 
This method is in charge of mapping data and visualising every
ideal function that has been obtained so that the user may see the error.
'''
def train_ideal(train_data, ideal_data, ideal_data_indices):
     
    plt.plot(train_data.rx_data(), train_data.ry_data(1), label="First train data y1")
    plt.plot(ideal_data.rx_data(), ideal_data.ry_data(ideal_data_indices[0]),
        color='red', label=f"Ideal function y{ideal_data_indices[0]}")
    plt.legend()
    plt.grid(True, color="k")
    plt.ylabel('Ideal Functions- y axis')
    plt.xlabel('Train Data- x axis')
    plt.title('First ideal function')
    plt.show()

    plt.plot(train_data.rx_data(), train_data.ry_data(2), label="Second train data y2")
    plt.plot(ideal_data.rx_data(), ideal_data.ry_data(ideal_data_indices[1]),
       color='red',  label=f"Ideal function y{ideal_data_indices[1]}")
    plt.legend()
    plt.grid(True, color="k")
    plt.ylabel('Ideal Functions- y axis')
    plt.xlabel('Train Data- x axis')
    plt.title('Second ideal function')
    plt.show()

    plt.plot(train_data.rx_data(), train_data.ry_data(3), label="Third train data y3")
    plt.plot(ideal_data.rx_data(), ideal_data.ry_data(ideal_data_indices[2]),
        color='red', label=f"Ideal function y{ideal_data_indices[2]}")
    plt.legend()
    plt.grid(True, color="k")
    plt.ylabel('Ideal Functions- y axis')
    plt.xlabel('Train Data- x axis')
    plt.title('Third ideal function')
    plt.show()

    plt.plot(train_data.rx_data(), train_data.ry_data(4), label="Fourth train data y4")
    plt.plot(ideal_data.rx_data(), ideal_data.ry_data(ideal_data_indices[3]),
        color='red', label=f"Ideal function y{ideal_data_indices[3]}")
    plt.legend()
    plt.grid(True, color="k")
    plt.ylabel('Ideal Functions- y axis')
    plt.xlabel('Train Data- x axis')
    plt.title('Fourth ideal function')
    plt.show()
    
def mapped_data(ideal_data, ideal_data_errors, ideal_data_indices, x_values, y_values, val):
    plt.plot(ideal_data.rx_data(), ideal_data.ry_data(ideal_data_indices[val - 1]), label="Ideal function")
    plt.plot(ideal_data.rx_data(),
             ideal_data.ry_data(ideal_data_indices[val - 1]) + (ideal_data_errors[val - 1] * np.sqrt(2)), 'k--',
             label="Error bounds")
    plt.plot(ideal_data.rx_data(),
             ideal_data.ry_data(ideal_data_indices[val - 1]) - (ideal_data_errors[val - 1] * np.sqrt(2)), 'k--')
    plt.scatter(x_values, y_values, color='y', label="Mapped train data")
    plt.legend()
    plt.grid(True, color="k")
    plt.ylabel('y axis')
    plt.xlabel('x axis')
    plt.title(f'{ordinal(val)} Ideal Function Mapping')
    plt.show()

def ordinal(n):
    suffix = 'th' if 11 <= n <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"