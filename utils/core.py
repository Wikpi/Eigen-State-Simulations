import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from typing import Callable

# Base simulation object
class Simulation:
    def __init__(self, well: Well) -> None:
        self.reset(well)

    # Resets the simulation to defaults
    def reset(self, well: Well) -> None:
        self.well: Well = well
        self.models: list = []
        self.axisX: list = []
        self.dx: float = 0
        self.solutions: list = []

    # Add a new model function reference
    def addModel(self, model: Callable[[float], float]) -> None:
        self.models.append(model)

    # Defines a new grid for the simulation
    def grid(self, xMin: float, xMax: float, xStep: float) -> None:
        self.axisX = np.linspace(xMin, xMax, xStep)
        self.dx = self.axisX[1] - self.axisX[0]

    # Runs the simulation
    def run(self, plot: bool = False) -> list:
        self.solutions = odeint(self.models, self.initialValues, self.axisX, args=()) # Pass needed args later

        if plot:
            self.plot()

        return self.solutions

    # Normalizes simulation results
    def normalize(self) -> None:
        return

    # Plots the simulation
    def plot(self) -> None:
        plt.plot(axisX, self.solutions, label="")
        
        plt.xlabel("")
        plt.ylabel("")
        plt.title("")
        
        plt.grid(True)
        plt.show()

# Base well potential object
class Well:
    def __init__(self) -> None:
        return