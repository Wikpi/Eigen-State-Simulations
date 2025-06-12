import math as math
import numpy as np
from numpy.typing import NDArray
import util.simulation as sm
import util.solution as sl
import util.core as core
import util.bracket as br

# Creating a class for the harmonic oscillator model
class HarmonicOscillator(sm.ModelSystem):
    """Base model system object class. Adapted to model the Harmonic Oscillator as per project description.

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   dataPath: str           - path to simulation data
    """

    # Harmonic Oscillator model constructor
    def __init__(self) -> None:
        self.label: str = "Harmonic Oscillator"
        self.dataPath: str = "simulations/harmonic-oscillator/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    # Defining the model system function as per the differential equations provided
    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon: float) -> list:

        y1 , y2 = y # Unpacking psi and psi'

        return[y2, (0.25 * (x**2) - epsilon) * y1] # Returns rhs values of the system differential equations for psi' and psi''
    
# Defining a function to find the epsilon brackets that we can use to find the valid solutions
def findSolutionBrackets(model: sm.ModelSystem, xValues: NDArray, epsilonRange: NDArray, parity: str) -> dict[tuple[float, float], str]:
    """ 
        `findSolutionBrackets` searches over a given range of `epsilon` values and returns a `dict` containing the 
        epsilon bracket ranges where solutions of a given `parity` may be found, paired with the parity.
    """

    # From the epsilon range compute a new epsilon list full of epsilon objects
    epsilonList: list = []
    for epsilon in epsilonRange:
        epsilonList.append(core.Epsilon(epsilon, parity))
    
    # Solutions for all epsilons in list
    solutions: list[sl.Solution] = core.solveEpsilonList(model, xValues, epsilonList)

    # Initialising list of endpoints of sampled solutions
    yEndpoints: list = []
    # Solving the wavefunction for the sampled epsilons assuming initial conditions according to parity, and storing the endpoint values in a list
    for solution in solutions:
        yEndpoints.append(solution.result[-1])

    # Computed brackets
    solutionBrackets: [br.Bracket] = []

    # Checking where the endpoint changes sign, and storing those epsilon ranges as tuples paired with solution parity
    for i in range(np.size(epsilonRange) - 1):
        if yEndpoints[i + 1] * yEndpoints[i] < 0:
            newBracket: br.Bracket = br.Bracket(epsilonRange[i], epsilonRange[i + 1], parity)

            solutionBrackets.append(newBracket)
    
    return solutionBrackets

# Specifying xValue range and step
xMin: float = 0
xMax: float = 7
xStep: float = 0.005
xValues: NDArray = np.linspace(xMin, xMax, int(xMax/xStep))

# Specifying epsilon range and step
epsilonMin: float = 0
epsilonMax: float = 5
epsilonStep: float = 0.01
epsilonRange: NDArray = np.linspace(epsilonMin, epsilonMax, int(epsilonMax/epsilonStep))

def main() -> None:
    # Defining HarmonicOscillator modelSystem
    model : HarmonicOscillator = HarmonicOscillator()

    # Defining simulation 
    simulation: sm.Simulation = sm.Simulation()
    simulation.modifyGrid(xMin, xMax, xStep, xLabel="$Position  \\xi  (Dimensionless)$", yLabel="$Wavefunction y_1 Values")

    # Specifying simulation parameters, particularly for the bracketEnergyState() function
    model.iterationCount = 32
    model.approximation = 1e-16

    # Combining the odd and even solution backets into one dictionary
    solutionBrackets: list[br.Bracket] = []

    # Finding the odd and even solution brackets
    evenBrackets: list[br.Bracket] = findSolutionBrackets(model, xValues, epsilonRange, "even")
    oddBrackets: list[br.Bracket] = findSolutionBrackets(model, xValues, epsilonRange, "odd")
    
    solutionBrackets.extend(evenBrackets)
    solutionBrackets.extend(oddBrackets)

    # Editing the simulation title to match the number of solutions found
    simulation.title = "%s bracket simulation: first %d solutions"%(model.label, len(solutionBrackets))

    # Running the bracket simulation for the solution brackets found
    sm.bracketSimulation(simulation, model, solutionBrackets, plot=True)

    print("Done running the %s simulation." % model.label)

    return

main()   
