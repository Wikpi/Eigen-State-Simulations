import math
import numpy as np
from numpy.typing import NDArray
import util.solution as sl

# One of simulation computations.
def bracketEnergyState(model: "simulation.ModelSystem", xValues: NDArray, epsilonList: list) -> None:
    """`bracketEnergyState` finds the energy state approximation using bracketing method based on the `model` and `epsilonList[epsilonHigh, epsilonLow]`"""
    
    solutions: list = []

    # Epsilons list is composed of 2 epsilon initial predictions
    epsilonLow, epsilonHigh = epsilonList
    
    iterationCtx: int = 20 # Default iteration count, in the case that the model does not provide a specified count
    if hasattr(model, "iterationCount") and model.iterationCount > 0:
        iterationCtx = model.iterationCount

    approximatation: int = 1e-6 # Default approximatation, in the case that the model does not provide a specified approximatation
    if hasattr(model, "approximatation"):
        approximatation = model.approximatation

    for i in range(iterationCtx):
        # If prediction gap is already smaller than `approximation` then its good enough
        if abs(epsilonHigh - epsilonLow) < approximatation:
            break

        # Midpoint in the prediction gap - current approximation
        epsilonMid: float = (epsilonHigh + epsilonLow) / 2
        
        solutionLow: list = sl.getSolution(model, xValues, epsilonLow, True)
        solutionHigh: list = sl.getSolution(model, xValues, epsilonHigh, True)
        solutionMid: list = sl.getSolution(model, xValues, epsilonMid, True)
        
        # Depending on what solution is at the wall (where lim x -> L and function 'vanishes), adapt the bounding prediction limits
        if np.sign(solutionMid.normalised[-1]) == np.sign(solutionHigh.normalised[-1]):
            epsilonHigh = epsilonMid
        else:
            epsilonLow = epsilonMid
    
    # Return back the last made approximation through bracketing
    solutions.extend([solutionHigh, solutionLow])

    return solutions

# One of simulation computations. 
def solveEpsilonList(model: "simulation.ModelSystem", xValues: NDArray, epsilonList: list) -> list:
    """`solveEpsilonList` computes the solutions for the given `model` and `epsilonList`"""
    
    solutions: list = [] 
    
    # Check every epsilon for solution
    for epsilon in epsilonList:
        try:
            # Compute a new normalised solution
            newSolution: solution.Solution = sl.getSolution(model, xValues, epsilon, True)

            solutions.append(newSolution)
        except ValueError as error:
            # Getting an error from a specific solution should not be fatal to the whole simulation, therefore just notify the user
            print("Warning computing solution: %s" % error)
        
    return solutions

# Determine the wavefunction type: odd or even.
def checkWavefunctionEvenOdd(epsilon: float) -> str:
    """`checkWavefunctionEvenOdd` determines whether the wavefunction is odd or even.
        This is based on the fact: `epsilon = pow(n, 2)` and if `n` is even the
        wavefunction will be odd, if `n` odd then the wavefunction will be even. 
    """

    if round(math.sqrt(epsilon)) % 2 == 0:
        return "odd"
    else:
        return "even"