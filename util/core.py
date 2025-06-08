import math
import numpy as np
from numpy.typing import NDArray
import util.solution as sl
from scipy.optimize import fsolve
import util.simulation as sm

# One of simulation computations.
def bracketEnergyState(model: "simulation.ModelSystem", xValues: NDArray, bracketList: list) -> None:
    """`bracketEnergyState` finds the energy state approximation using bracketing method based on the `model` and `bracketList[[epsilonHigh, epsilonLow]...]`"""
    
    solutions: list = []
    
    iterationCtx: int = 20 # Default iteration count, in the case that the model does not provide a specified count
    if hasattr(model, "iterationCount") and model.iterationCount > 0:
        iterationCtx = model.iterationCount

    approximatation: int = 1e-6 # Default approximatation, in the case that the model does not provide a specified approximatation
    if hasattr(model, "approximatation"):
        approximatation = model.approximatation

    for (epsilonLow, epsilonHigh) in bracketList:
        for i in range(iterationCtx):
            # If prediction gap is already smaller than `approximation` then its good enough
            if abs(epsilonHigh - epsilonLow) < approximatation:
                break

            # Midpoint in the prediction gap - current approximation
            epsilonMid: float = (epsilonHigh + epsilonLow) / 2
            
            solutionLow: sl.Solution = sl.getSolution(model, xValues, epsilonLow, True)
            solutionHigh: sl.Solution = sl.getSolution(model, xValues, epsilonHigh, True)
            solutionMid: sl.Solution = sl.getSolution(model, xValues, epsilonMid, True)
            
            # Depending on what solution is at the wall (where lim x -> L and function 'vanishes), adapt the bounding prediction limits
            if np.sign(solutionMid.normalised[-1]) == np.sign(solutionHigh.normalised[-1]):
                epsilonHigh = epsilonMid
            else:
                epsilonLow = epsilonMid
        
        epsilonRoot = (epsilonHigh + epsilonLow) / 2
        solution: sl.Solution = sl.getSolution(model, xValues, epsilonRoot, True)

        # Append the last made approximation through bracketing
        solutions.append(solution)

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

def evenModel(z, z0) -> NDArray:
    return np.sqrt(z0**2 - z**2) - z * np.tan(z)

# for even solutions (n = 1,3,5,…)
def evenGuesses(z0: float) -> list:
    return [(2*k-1)*np.pi/2 for k in range(1, int(z0/np.pi)+1)]

def oddModel(z, z0) -> NDArray:
    with np.errstate(divide='ignore', invalid='ignore'): # since the denominator is alwasy really close to 0
        return np.sqrt(z0**2 - z**2) + z / np.tan(z)

# for odd solutions (n = 2,4,6,…)
def oddGuesses(z0: float) -> list:
    return [k*np.pi for k in range(1, int(z0/np.pi)+1)]

# Finds roots of function with initial guess.
def findRoots(function, guesses, z0) -> list:
    roots: list = []

    for guess in guesses:
        root, info, ier, _ = fsolve(lambda z: function(z, z0), guess, full_output=True)
        # Check if valid
        if ier != 1 or 0 >= root or root >= z0:
            continue

        # avoid duplicates within tolerance
        if any(np.isclose(root, s, atol=1e-4) for s in roots):
            continue

        roots.append(root[0])

    return sorted(roots)

def computeBrackets(roots: list, margin: float = 1e-2) -> list:
    brackets: list = []

    for root in roots:
        # Convert z into epsilon vlaues: epsilon = (2 * z / pi) ** 2
        epsilon = (2 * root / np.pi)**2

        # Compute marginalised brackers
        brackets.append((epsilon - margin, epsilon + margin))

    return brackets

def findEnergy(model: "sm.ModelSystem", z0: float, xValues: NDArray) -> float:
    solutions: list = []

    evenRoots = findRoots(evenModel, evenGuesses(z0), z0)
    evenBrackets = computeBrackets(evenRoots)
    
    oddRoots = findRoots(oddModel, oddGuesses(z0), z0)
    oddBrackets = computeBrackets(oddRoots)
    
    fullBrackets = evenBrackets + oddBrackets

    # Even though we found roots, it would be better to bracket through and approxiamte the solution even further
    solutions = bracketEnergyState(model, xValues, fullBrackets)

    return solutions