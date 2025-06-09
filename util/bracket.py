# Pakcage imports
from numpy.typing import NDArray
from scipy.constants import pi
import numpy as np

# Custom imports
import util.core as core
import util.solution as sl

class Bracket:
    """
        Base bracket object class.

        Class variables:
         #   low: float  - bracket initial low end
         #   high: float - bracket initial high end
         #   parity: str - bracket parity type: odd or even
    """

    def __init__(self, low: float, high: float, parity: str):
        self.reset()

        self.low = low
        self.high = high
        self.parity = parity

    def reset(self):
        self.low = 0
        self.high = 0
        self.parity = ""

# One of simulation computations.
def bracketEnergyState(model: "simulation.ModelSystem", xValues: NDArray, bracketList: list[Bracket]) -> list[sl.Solution]:
    """`bracketEnergyState` finds the energy state approximation using bracketing method based on the `model` and `bracketList[[epsilonHigh, epsilonLow]...]`"""
    
    # Final bracketed epsilon approximations
    epsilonRoots: list[core.Epsilon] = []
    
    iterationCtx: int = 20 # Default iteration count, in the case that the model does not provide a specified count
    if hasattr(model, "iterationCount") and model.iterationCount > 0:
        iterationCtx = model.iterationCount

    approximatation: int = 1e-6 # Default approximatation, in the case that the model does not provide a specified approximatation
    if hasattr(model, "approximatation"):
        approximatation = model.approximatation

    # Compute all brackets
    for bracket in bracketList:
        epsilonRoot: float = solveBracket(model, bracket, xValues, iterationCtx, approximatation)
        
        newEpsilon: core.Epsilon = core.Epsilon(epsilonRoot, bracket.parity)

        epsilonRoots.append(newEpsilon)

    solutions: list[sl.Solution] = core.solveEpsilonList(model, xValues, epsilonRoots)

    return solutions

# Computes the mid epsilon for a specifc bracket.
def solveBracket(model: "sm.ModelSystem", bracket: Bracket, xValues: NDArray, iterationCtx: int, approximatation: float) -> float:
    """`solveBracket` computes the approximated root epsilon value for the given `bracket`."""
    
    # Retrieve bracket immediate info
    epsilonLow, epsilonHigh, parity = bracket.low, bracket.high, bracket.parity

    # Approximated root epsilon
    epsilonRoot: float = 0

    for i in range(iterationCtx):
        # If prediction gap is already smaller than `approximation` then its good enough
        if abs(epsilonHigh - epsilonLow) < approximatation:
            break

        # Midpoint in the prediction gap - current approximation
        epsilonRoot = (epsilonHigh + epsilonLow) / 2
        
        solutionHigh: sl.Solution = sl.getSolution(model, xValues, epsilonHigh, True, parity)
        solutionMid: sl.Solution = sl.getSolution(model, xValues, epsilonRoot, True, parity)
        
        # Depending on what solution is at the wall (where lim x -> L and function 'vanishes), adapt the bounding prediction limits
        if np.sign(solutionMid.result[-1]) == np.sign(solutionHigh.result[-1]):
            epsilonHigh = epsilonRoot
        else:
            epsilonLow = epsilonRoot
    
    return epsilonRoot

# Make bracket pairs from computed values.
def computeBrackets(roots: list[float], bracketType: str, margin: float = 1e-2) -> list[Bracket]:
    """`computeBrackets` creates brackets for each found root in `roots` within the `margin`."""
    
    # Initialised empty brackets list
    brackets: list[Bracket] = []

    # Compute new brackets for every found root/value
    for root in roots:
        # Convert z into epsilon vlaues: epsilon = (2 * z / pi) ** 2
        epsilon: float = (2 * root / pi)**2

        # Compute marginalised brackets
        newBracket: Bracket = Bracket(epsilon - margin, epsilon + margin, bracketType)

        brackets.append(newBracket)
        
    return brackets