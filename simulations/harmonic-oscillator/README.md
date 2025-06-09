# Main Project

# Quantum-Harmonic-Oscillator

## Description

The project simulates the Harmonic Oscillator using a model class that behaves as dictated by the appropriate differential equations. In order to find the energy levels for which the solution tends to 0 as x tends to infinity, we first find epsilon ranges (`brackets`) within which the solution to the differential equations change their sign at the end points. Consequently, we can infer that there must exist solutions within these epsilon ranges where the endpoint of the solution becomes zero. These are the solutions that we want to find and plot.  

The program first specifies the extent of x values across which this process is executed. Note that reducing the maximum x value significantly may affect the accuracy of the program, and lead to incorrect results.

Then, a range of epsilon values is specified, across which the brackets are found. Note that changing the maximum range of epsilon values will effect the number of solutions found. Due to the nature of the system, it so happens that the number of solutions found corresponds to the rounded value of the mazimum epsilon value. Thus, for a range of [0, 5], you should find 5 brackets and consequently, 5 solutions. Changing the epsilon step shouldn't affect the program much as long as it remains less than 0.5, after which it may lead to incorrect results.

Once the brackets are found, a simulation is run to find the required solutions contained within them, using the bracketing method. These solutions are then stored and plotted, labelled with their corresponding epsilon values. The plot can be dound in `harmonic-oscillator/data`.

## Requirements

- Python 3.8 or later  
- NumPy  
- SciPy  
- Matplotlib

## Usage

* From project root directory run the specified makefile simulation command:

    > `make harmonic`










