# Package imports
import math
import numpy as np
from numpy.typing import NDArray
from scipy.optimize import fsolve
from scipy.constants import pi

# Custom imports
import util.solution as sl
import util.simulation as sm
import util.bracket as br

class Epsilon:
    """
        Base epsilon object class.

        Class variables:
         #   value: float - epsilon value
         #   parity: str  - epsilon parity
    """

    def __init__(self, value: float, parity: str):
        self.reset()

        self.value = value
        self.parity = parity

    def reset(self) -> None:
        self.value = 0
        self.parity = ""

# One of simulation computations. 
def solveEpsilonList(model: "simulation.ModelSystem", xValues: NDArray, epsilonList: list[Epsilon]) -> list[sl.Solution]:
    """`solveEpsilonList` computes the solutions for the given `model` and `epsilonList`"""
    
    # Final solutions list initialisation
    solutions: list[sl.Solution] = [] 

    # Check every epsilon for solution
    for epsilon in epsilonList:
        try:
            # Compute a new normalised solution
            newSolution: sl.Solution = sl.getSolution(model, xValues, epsilon.value, True, epsilon.parity)

            solutions.append(newSolution)
        except ValueError as error:
            # Getting an error from a specific solution should not be fatal to the whole simulation, therefore just notify the user
            print("Warning computing solution: %s" % error)
        
    return solutions

# Finds roots of function with initial guess.
def findRoots(function, guesses, z0) -> list[float]:
    """`findRoots` finds solutions where `function` is zero (roots) for initial `guesses` and `z0` value."""
    
    roots: list[float] = []

    # Find roots for every computed guess
    for guess in guesses:
        root, info, ier, _ = fsolve(function, guess, args=(z0,), full_output=True)
        
        # Check if valid
        if ier != 1:
            continue

        # Avoid duplicates within small tolerance
        if any(np.isclose(root, s, atol=1e-4) for s in roots):
            continue

        roots.append(root[0])

    return roots