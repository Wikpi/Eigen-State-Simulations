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
        #   type: str               - type of model simulation: solve or bracket
        #   dataPath: str           - path to simulation data
    """

    # Abstract object constructor.
    def __init__(self) -> None:
        self.label: str = "New Model System" # Abstract non-empty model label
        self.type: str = "solve"
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

    # Run the simulation
    def run(self, epsilonList: list, plot: bool = False) -> list:
        """`run` starts the simulation, computes the solutions for the given system model and based on `plot` displays the solution graphs."""
        
        if self.model is None:
            return ValueError("No model given for the simulation.")

        if self.xValues.size == 0:
            return ValueError("Simulation space was not defined.")

        # Clear previous simulation results before starting a new simulation
        self.solutions.clear()

        # Run over all provided epsilon values
        if hasattr(self.model, "type") and self.model.type == "bracket":
            self.solutions = core.bracketEnergyState(self.model, self.xValues, epsilonList)
        else:
            self.solutions = core.solveEpsilonList(self.model, self.xValues, epsilonList)

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

# Helper script to simplify simulation running and debugging.
def runSimulation(simulation: Simulation, model: ModelSystem, epsilonList: list, plot: bool = False) -> list:
    """`runSImulation` simplifies simulation running by immediatly updating simulation model and handling errors."""
    
    result: list = []

    try:
        simulation.modifyModel(model)

        result = simulation.run(epsilonList, plot)
    except ValueError as error:
        print("Error running the simulation: %s" % error)

    return result