# Package imports
import numpy as np
from scipy.constants import pi
from numpy.typing import NDArray

# Custom imports
import util.simulation as sm
import util.core as core
import util.plot as plot

class FiniteWellPotential(sm.ModelSystem):
    """Base model system object class for finite well potential simulation.

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   dataPath: str           - path to simulation data
    """

    # Infinite well potential model constructor
    def __init__(self) -> None:
        self.label: str = "Finite Well Potential"
        self.dataPath: str = "simulations/well/finite/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon: float) -> list:
        """Finite Well Potential model system structure."""

        psi, dpsi = y # psi and psi derivative

        v = computeV(x)

        return [dpsi, pi**2 * (v - epsilon) * psi]

def computeV(x: float) -> NDArray:
    V0 = 1 # Some debug potential outside the well

    return np.piecewise(x, [np.abs(x) <= wellWall, np.abs(x) > wellWall], [0, V0])

def evenModel(z, z0) -> NDArray:
    return np.sqrt(z0**2 - z**2) - z * np.tan(z)

# For even solutions (n = 1,3,5,…)
def evenGuesses(z0: float) -> list:
    guesses = []

    # One solution per full scope of pi
    kMax = int(z0 / pi)

    for k in range(1, kMax + 1):
        guesses.append((2 * k - 1) * pi / 2)

    return guesses

def oddModel(z, z0) -> NDArray:
    with np.errstate(divide='ignore', invalid='ignore'): # since the denominator is always really close to 0
        return np.sqrt(z0**2 - z**2) + z / np.tan(z)

# For odd solutions (n = 2,4,6,…)
def oddGuesses(z0: float) -> list:
    guesses: list = []

    # One solution/guess per full scope of pi
    kMax = int(z0 / pi)

    # Compute all kMax guess (inclusive)
    for k in range(1, kMax + 1):
        guesses.append(k * pi)

    return guesses

# Computes the epsilon energy brackets for simulation.
def findEnergy(model: "sm.ModelSystem", z0: float, xValues: NDArray) -> list:
    evenRoots = core.findRoots(evenModel, evenGuesses(z0), z0)    
    oddRoots = core.findRoots(oddModel, oddGuesses(z0), z0)

    # Even though we found the roots, it would be better to bracket through and approxiamte the solution even further
    evenBrackets = core.computeBrackets(evenRoots)
    oddBrackets = core.computeBrackets(oddRoots)

    fullBrackets = evenBrackets + oddBrackets

    return fullBrackets

# The start value of integration
xMin: float = 0
# The well limit
wellWall: float = 0.5
# The end value of integration (for finite we define something beyond the wall: 2L, 3L...)
xMax: float = wellWall * 3
# The step value
xStep: float = 0.005

def main() -> None:
    model: FiniteWellPotential = FiniteWellPotential()

    simulation: sm.Simulation = sm.Simulation("%s Solve Simulation" % model.label)
    simulation.modifyGrid(xMin, xMax, xStep, wellWall, "v0 (Dimensionless)", "Wavefunction values")
    
    bracketList = []

    # Initial z0 list
    z0List = [1, 5, 8, 14]

    # Compute all epsilon brackets from initial z0
    for z0 in z0List:
        newStates = findEnergy(model, z0, simulation.xValues)

        bracketList.extend(newStates)

    # sm.bracketSimulation(simulation, model, bracketList, True)
    simulation.modifyModel(model)
    solutions = simulation.runBracket(bracketList, False)

    # Since solution object initializations are adapted for epsilons, need to hard change the labels into z0 here
    # Although could leave the epsilons as well, but would more obscure.
    for solution in solutions:
        z0 = round(pi / 2 * np.sqrt(solution.epsilon))

        solution.label = "z0 = %d" % z0

    simulation.solutions = solutions

    simulation.plot()

    return  

main()
