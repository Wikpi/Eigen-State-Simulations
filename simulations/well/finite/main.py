# Package imports
import numpy as np
from scipy.constants import pi
from numpy.typing import NDArray
import math

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

        v = computeV(x) # potential

        return [dpsi, pi**2 * (v - epsilon) * psi]

V0: float = 8.0 # Some debug potential outside the well

# Computes the potential.
def computeV(x: float) -> NDArray:
    """`computeV` returns piecewise smoothed function values based on `x`."""
    
    return np.piecewise(x, [np.abs(x) <= wellWall, np.abs(x) > wellWall], [0, V0])

# Model for even solutions.
def evenModel(z, z0) -> NDArray:
    """`evenModel` returns even model solutions for z values."""

    # sqrt(z0**2 + z**2) = z * tan(z)
    return np.sqrt(z0**2 - z**2) - z * np.tan(z)

# Guesses for even solutions (n = 1,3,5,…).
def evenGuesses(z0: float) -> list[float]:
    """`evenGuesses` computes all approximate estimates for even solutions."""
    
    guesses: list[float] = []
    
    # Generate (2k−1)*π/2 up through the last half-π before z0
    kMax: int = math.ceil(z0 / pi)
    for k in range(1, kMax + 1):
        guess: float = (2*k - 1) * pi / 2
    
        if guess < z0:
            guesses.append(guess)

    # ensure at least one for very shallow wells
    if not guesses and z0 > 0:
        guesses.append(z0 / 2)
    
    return guesses

# Model for odd solutions.
def oddModel(z, z0) -> NDArray:
    """`oddModel` returns odd model solutions for z values."""
    
    with np.errstate(divide='ignore', invalid='ignore'): # since the denominator is always really close to 0
        # sqrt(z0**2 + z**2) = -z / tan(z)
        return np.sqrt(z0**2 - z**2) + z / np.tan(z)

# Guesses for odd solutions (n = 2,4,6,…).
def oddGuesses(z0: float) -> list[float]:
    """`oddGuesses` computes all approximate estimates for odd solutions."""
    
    guesses: list[float] = []
    
    # Generate k*π up through the last π before z0
    kMax: int = math.ceil(z0 / pi)
    for k in range(1, kMax + 1):
        guess: float = k * pi

        if guess < z0:
            guesses.append(guess)

    return guesses

# Computes the epsilon energy brackets for simulation.
def findEnergy(model: "sm.ModelSystem", z0: float, xValues: NDArray) -> list[tuple[float, float]]:
    """`findEnergy` computes all even and odd epsilon energy brackets for a given `z0` and `model`."""
    
    evenRoots: list[float] = core.findRoots(evenModel, evenGuesses(z0), z0)    
    oddRoots: list[float] = core.findRoots(oddModel, oddGuesses(z0), z0)

    print("len of bound states for z0: ", len(evenRoots+oddRoots))

    # Even though we found the roots, it would be better to bracket through and approxiamte the solution even further
    evenBrackets: list[tuple[float, float]] = core.computeBrackets(evenRoots)
    oddBrackets: list[tuple[float, float]] = core.computeBrackets(oddRoots)

    fullBrackets: list[tuple[float, float]] = evenBrackets + oddBrackets

    return fullBrackets

# The start value of integration
xMin: float = 0
# The well limit
wellWall: float = 0.5
# The end value of integration (for finite we define something beyond the wall: 2L, 3L...)
xMax: float = wellWall * 3
# The step value
xStep: float = 0.005
# Initial z0 list
z0List: list[float] = [1, 5, 8, 14]

def main() -> None:
    # Initial finite well potential model used for the simulation
    model: FiniteWellPotential = FiniteWellPotential()

    # Simulation object with default/specified configuration
    simulation: sm.Simulation = sm.Simulation("%s Simulation for V0 = %.1f" % (model.label, V0))
    simulation.modifyGrid(xMin, xMax, xStep, wellWall, "v0 (Dimensionless)", "Wavefunction values")
    
    # List for holding computed brackets, which will be used to approximate bounding state solutions
    bracketList: list[tuple[float, float]] = []

    # Compute all epsilon brackets from initial z0
    for z0 in z0List:
        print("z0 = ", z0)
        newStates: list[tuple[float, float]] = findEnergy(model, z0, simulation.xValues)

        # Problem asks for 2 specific v0
        # if len(newStates) == 1 or len(newStates) == 2 or len(newStates) == 4:
        #     v0 = (2 * z0 / pi)**2

        #     print("v0 = %.2f has %d bounding states." % (v0 , len(newStates)))

        bracketList.extend(newStates)

    # sm.bracketSimulation(simulation, model, bracketList, True)
    simulation.modifyModel(model)
    solutions = simulation.runBracket(bracketList, False)

    # Since solution object initializations are adapted for epsilons, need to hard change the labels into z0 here
    # Although could leave the epsilons as well, but would be more obscure.
    for solution in solutions:
        z0: float = pi / 2 * np.sqrt(solution.epsilon)

        solution.label = "z0 = %.2f" % z0

    simulation.solutions = solutions

    simulation.plot()

    print("Done running the %s simulation." % model.label)

    return  

main()
