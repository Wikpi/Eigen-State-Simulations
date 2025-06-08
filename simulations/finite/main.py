from scipy.constants import pi
from scipy.constants import hbar
import util.simulation as sm
import numpy as np
from numpy.typing import NDArray
import util.core as core
import util.plot as plot

class FiniteWellPotential(sm.ModelSystem):
    """Base model system object class for finite well potential simulation.

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   type: str               - type of model simulation: solve or bracket
        #   dataPath: str           - path to simulation data
    """

    # Infinite well potential model constructor
    def __init__(self) -> None:
        self.label: str = "Finite Well Potential"
        self.type: str = "solve"
        self.V0: float = 8.0
        self.dataPath: str = "simulations/finite/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    

    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon: float) -> list:
        """Finite Well Potential model system structure."""

        psi, dpsi = y # psi and psi derivative
        V0 = 8

        v = computeV(x)

        return [dpsi, pi**2 * (v - epsilon) * psi]

# The start value of integration
xMin: float = 0
# The well limit
wellWall: float = 0.5
# The end value of integration (for finite we define something beyond the wall: 2L, 3L...)
xMax: float = wellWall * 3
# The step value
xStep: float = 0.005

V0 = 8

def computeV(x: float) -> NDArray:
    return np.piecewise(x, [np.abs(x) <= wellWall, np.abs(x) > wellWall], [0, V0])

def main() -> None:
    model: FiniteWellPotential = FiniteWellPotential()

    simulation: sm.Simulation = sm.Simulation("%s Solve Simulation" % model.label)
    simulation.modifyGrid(xMin, xMax, xStep, wellWall, "Position x/L (Dimensionless)", "Wavefunction values")
    
    # Epsilon list to find solutions for
    # epsilonList: list = [1, 4, 9, 16]

    # Solve system of ODEs for epsilon list
    # sm.runSimulation(simulation, model, epsilonList, True)
    
    epsilonList = []

    z0List = [1, 5, 8, 14]
    for z0 in z0List:
        newEpsilon = core.findEnergy(model, z0, simulation.xValues)

        epsilonList.append(newEpsilon)

    # print(epsilonList)

    # Clear the graph of preivous simulation
    plot.clearGraph()

    # Configure new simulation graph parameters
    plot.configureGraph("new simulation", "x", "y", True)

    # Graph every solution
    for epsilon in epsilonList:
        for solution in epsilon:
            plot.plotGraph(simulation.xValues, solution.normalised, solution.label, solution.type)

    plot.saveGraph(model.dataPath, "new title")

    # Display the graph
    plot.displayGraph()

    return  

main()
