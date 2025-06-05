import scipy.integrate as calculus
import scipy.constants as constants
import matplotlib.pyplot as plt
import numpy as np
import math 

#Defining the functions for the warm up problem
#The system of equations are given by dy1/dx and dy2/dx, where y1 is the wave function and y1' = y2 
def infinite_well_potential(x,y, epsilon):
    y1 , y2 = y
    dy1dt =  y2
    dy2dt = (-(constants.pi ** 2) * epsilon * y1)
    return [dy1dt, dy2dt]

#Defining separate functions to evaluate the odd and even solutions according to their initial conditions
def get_even_wavefunction(epsilon, step):
    x_span = (0,0.5)
    x_eval = np.linspace(0,0.5,int(0.5/step))
    initial_even = [1,0]
    solution = calculus.solve_ivp(infinite_well_potential, t_span=x_span, t_eval = x_eval, y0 = initial_even, args = (epsilon,))
    return solution

def get_odd_wavefunction(epsilon,step):
    x_span = (0,0.5)
    x_eval = np.linspace(0,0.5,int(0.5/step))
    initial_odd = [0,1]
    solution = calculus.solve_ivp(infinite_well_potential, t_span=x_span, t_eval = x_eval, y0 = initial_odd, args = (epsilon,))
    return solution

#Defining a function that will normalise a given set of input output pairs (arrays) by finding the approximate integral
def normalise_output(x_values, y_values):
    #Area with rectangles below the graph
    lower_integral = 0
    for i in range(np.size(x_values)-1):
        dx = math.fabs(x_values[i + 1] - x_values[i])
        dy = y_values[i]**2
        lower_integral += dy * dx
    #Area with rectangles above the graph
    upper_integral = 0
    for i in range(np.size(x_values)-1):
        dx = math.fabs(x_values[i + 1] - x_values[i])
        dy = y_values[i+1]**2
        upper_integral += dy * dx    
    #The normalisation factor is given by sqrt(integral value)*2 (when evaluated for x = 0 to x = 0.5)
    #The average of the upper and lower bound integral is used for additional accuracy
    normalisation_factor = (upper_integral**0.5 + lower_integral**0.5) #the average is not divided by 2 because the function is only called for the y1 values from 0 to 0.5
    print(normalisation_factor)
    y_values_normalised = y_values/(normalisation_factor)

    return y_values_normalised

def plot_even_wavefunction(epsilon, step):
    solution = get_even_wavefunction(epsilon, step)
    print(solution)
    x_values = solution.t
    y1_values = normalise_output(x_values, solution.y[0])

    #Obtaining the negative x half of the even function
    negative_x_values = -1*x_values[ : 0 : -1]
    negative_y1_values = y1_values[ : 0 : -1]

    #Combining the values to get the full function values from -L to L
    plot_x_values = np.concatenate((negative_x_values, x_values) )
    plot_y1_values = np.concatenate((negative_y1_values, y1_values) )

    #Plotting the full wavefunction
    plt.plot(plot_x_values, plot_y1_values, label = "$\epsilon =$ %d"%(epsilon))

def plot_odd_wavefunction(epsilon,step):
    solution = get_odd_wavefunction(epsilon, step)
    print(solution)
    x_values = solution.t
    y1_values = normalise_output(x_values, solution.y[0])

    #Obtaining the negative x half of the even function
    negative_x_values = -1*x_values[ : 0 : -1]
    negative_y1_values = -y1_values[ : 0 : -1]

    #combining the values to get the full function values from -L to L
    plot_x_values = np.concatenate((negative_x_values, x_values) )
    plot_y1_values = np.concatenate((negative_y1_values, y1_values) )

    #Plotting the full wavefunction
    plt.plot(plot_x_values, plot_y1_values, label = "$\epsilon =$ %d"%(epsilon))

#main
#The valid solutions are the odd solutions for n = 2, 4 and the even solutions for n = 1, 3; as they have y1 aproaching 0 at the endpoints
epsilon_test_values = [1, 4, 9, 16]
step = 0.005
#Loop that will plot each of the valid solutions 
for epsilon in epsilon_test_values:
    if math.sqrt(epsilon)%2 == 0:#if n in epsilon_n is even
       plot_odd_wavefunction(epsilon, step)
    else:
       plot_even_wavefunction(epsilon, step)
plt.title("Wavefunction for a particle in an infinite well potential")
plt.xlabel("Position x/L (Dimensionless)")
plt.ylabel("Function Values")
plt.legend()
plt.grid(True)
plt.show()