from numpy.typing import NDArray
from scipy.integrate import odeint
import numpy as np
import util.core as core
import math

# Base solution object class
class Solution:
    """Base solution object class.

       Class variables:
        #   label: str          - name of the solution (used to differentiate the solution when plotting)
        #   result: NDArray     - the solution of the ode itself
        #   epsilon: float      - the specific epsilon value corresponding to the solution

        #   type: int           - specifies whether the solution is even (=1) or odd (=-1)
        #   normalised: NDArray - the normalized ode solution result
    """

    # Object constructor with optional values
    def __init__(self, label: str = "", result: NDArray = [], epsilon = 0) -> None:
        self.reset()

        if label != "":
            self.label = label

        if result.size != 0:
            self.result = result

        if epsilon != 0:
            self.epsilon = epsilon

    # Reset the solution.
    def reset(self) -> None:
        """`reset` reverts the solution to default values."""

        self.label: str = "New Solution" # Abstract non-empty label
        self.result: NDArray = np.array([])
        self.normalised: NDArray = np.array([])
        self.epsilon = 0

    # Normalise the solution.
    def normalise(self, xValues: NDArray) -> NDArray:
        """`normalise` normalises the solution results."""

        if self.result.size == 0:
            return ValueError("Cannot normalise solution %s: the solution has not been computed or is missing its result data." % self.label)

        self.normalised =  normaliseSolution(xValues, self.result)

        return self.normalised

# Compues a new model solution.
def getSolution(model: "simulation.ModelSystem", xValues: NDArray, epsilon: float, normalise: bool = False) -> Solution:
    """`getSolution` computes a new solution result based on the provided `model` and `epsilon` values"""
    
    # Determine the type of solution: odd / even
    solutionType: str = core.checkWavefunctionEvenOdd(epsilon)

    # Solution results
    solutionResult: NDArray = odeint(model.system, model.getInitialConditions(solutionType), xValues, args=(epsilon,))

    # Configure new solution class object
    newSolution: Solution = Solution("$\\epsilon$ = %.1f" % epsilon, solutionResult[:, 0])
    newSolution.type = solutionType

    # Most of the time we want to get normalised results
    if normalise:
        newSolution.normalise(xValues)

    return newSolution

# Normalise given values.
def normaliseSolution(xValues: NDArray, yValues: NDArray) -> NDArray:
    """`normaliseSolution` normalises the given function values by finding the approximate integral."""
    
    #Area with rectangles below the graph
    lowerIntegral: float = integrateSolution(xValues, yValues, "lower")
    
    #Area with rectangles above the graph
    upperIntegral: float = integrateSolution(xValues, yValues, "upper")
    
    #The average of the upper and lower bound integral is used for additional accuracy
    approxIntegral : float = (lowerIntegral + upperIntegral)/2
    
    #The normalisation factor is given by sqrt(2 * integral value) (when evaluated for x = 0 to x = L)
    normalisationFactor: float = math.sqrt(2 * approxIntegral) 

    return yValues / normalisationFactor

# Simple integration method.
def integrateSolution(xValues: NDArray, yValues: NDArray, type: str = "lower") -> float:
    """`integrateSolution` integrates function using rectangular method. \n
        type can be set to 'upper' or 'lower'
    """

    integral: float = 0
    
    #Configure function type as upper or lower
    if type == "lower":
        x = 0
    elif type == "upper":
        x = 1

    # Add up the rectangles
    for i in range(xValues.size - 1):
        dx = math.fabs(xValues[i + 1] - xValues[i])
        dy = yValues[i + x]**2 #the x value determines if the upper or lower integral is calculated

        integral += dy * dx

    return integral