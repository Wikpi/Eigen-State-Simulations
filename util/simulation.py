import numpy as np
from numpy.typing import NDArray
import util.plot as plot
import util.core as core

# Base model system object class.
class ModelSystem:
    """Base model system object class. Should be inherited and adapted per simulation.

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   dataPath: str           - path to simulation data
    """

    # Abstract object constructor.
    def __init__(self) -> None:
        self.label: str = "New Model System" # Abstract non-empty model label
        self.dataPath: str = "data"
        self.initialConditions: dict = {
            "odd": [],
            "even": []
        }

    # Abstract model system.
    def system(self) -> list:
        """Model system structure."""

        return []

    # Determine class initial conditions.
    def getInitialConditions(self, type: str) -> list:
        """Adapt model system initial conditions based on given `type`."""

        return self.initialConditions[type]

# Base simulation object
class Simulation:
    """Base simulation object class.

       Class variables:
        #   title: str          - name of the simulation
        #   xLabel: str         - horizontal axis label
        #   yLabel: str         - vertical axis label
        #   xValues: NDArray      - list of all horizontal axis points
        #   model: ModelSystem  - model functions for which the solution was found

        #   solutions: list[Solution] - all computed solutions of the model system
    """

    # Object constructor with optional values.
    def __init__(self, title: str = "") -> None:
        self.reset()
        
        if title != "":
            self.title = title

    # Resets the simulation.
    def reset(self) -> None:
        """`reset` reverts the simulation to default values."""
        
        self.title: str = "New Simulation" # Abstract non-empty simulation title
        self.xLabel: str = "x (dimensionless)" # Abstract non-empty x axis label
        self.yLabel: str = "y (dimensionless)" # Abstract non-empty y axis label
        self.xValues: NDArray = np.array([])
        self.wellWall: float = 0
        self.model: ModelSystem = None
        self.initialValues: list = []
        self.solutions: list = []

    # Define a new simulation space.
    def modifyGrid(self, xMin: float, xMax: float, xStep: float, wellWall: float, xLabel: str = "", yLabel: str = "") -> None:
        """`modifyGrid` defines a new simulation space."""
        
        # Overall simulation integration range
        self.xValues = np.linspace(xMin, xMax, int(xMax/xStep))
        # The well wall
        self.wellWall

        if xLabel != "":
            self.xLabel = xLabel

        if yLabel != "":
            self.yLabel = yLabel

    # Change the simulation model.
    def modifyModel(self, model: ModelSystem) -> None:
        """`modifyModel` defines a new simulation system model."""
        
        self.model = model

    # Clear the simulation of any results.
    def clearSolutions(self) -> None:
        """`clearSOlutions` removes any residual solutions left from previous simulatopn attempts."""

        self.solutions.clear()

    # Run the simulation solving method.
    def runSolve(self, epsilonList: list, plot: bool = False) -> list:
        """`runSolve` runs the simulation in solving mode."""
        
        if self.model is None:
            return ValueError("No model given for the simulation.")

        if self.xValues.size == 0:
            return ValueError("Simulation space was not defined.")

        self.clearSolutions()

        self.solutions = core.solveEpsilonList(self.model, self.xValues, epsilonList)

        # Plotting is optional
        if plot:
            self.plot()

        return self.solutions

    # Run the simulation bracketing method.
    def runBracket(self, bracketList: list, plot: bool = False) -> list:
        """`runBracket` runs the simulation in bracketing mode."""
        
        if self.model is None:
            return ValueError("No model given for the simulation.")

        if self.xValues.size == 0:
            return ValueError("Simulation space was not defined.")

        self.clearSolutions()

        self.solutions = core.bracketEnergyState(self.model, self.xValues, bracketList)

        # Plotting is optional
        if plot:
            self.plot()

        return self.solutions

    # Plot the solutions of the simulation
    def plot(self) -> None:
        """`plot` configures the graphs and displays the computed simulation solutions."""

        # Clear the graph of preivous simulation
        plot.clearGraph()

        # Configure new simulation graph parameters
        plot.configureGraph(self.title, self.xLabel, self.yLabel, True)

        # Graph every solution
        for solution in self.solutions:
            plot.plotGraph(self.xValues, solution.normalised, solution.label, solution.type)

        plot.saveGraph(self.model.dataPath, self.title)

        # Display the graph
        plot.displayGraph()

def solveSimulation(simulation: Simulation, model: ModelSystem, epsilonList: list, plot: bool = False) -> list:    
    result: list = []

    try:
        simulation.modifyModel(model)

        result = simulation.runSolve(epsilonList, plot)
    except ValueError as error:
        print("Error solving the simulation: %s" % error)

    return result

def bracketSimulation(simulation: Simulation, model: ModelSystem, bracketList: list, plot: bool = False) -> list: 
    result: list = []

    try:
        simulation.modifyModel(model)

        result = simulation.runBracket(bracketList, plot)
    except ValueError as error:
        print("Error bracketing the simulation: %s" % error)

    return result