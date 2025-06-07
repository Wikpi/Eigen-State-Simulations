import matplotlib.pyplot as plt
from numpy.typing import NDArray
import numpy as np
import os

# Clear graph.
def clearGraph() -> None:
    """`clearGraph` clears the current simulation graph of any inserted values."""

    plt.clf()

# Congiure graph parameters.
def configureGraph(title: str, xLabel: str, yLabel: str, showGrid: bool = False) -> None:
    """`configureGraph` sets simulation graph parameters."""
    
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    
    plt.grid(showGrid)

# Plot the simulation graph.
def plotGraph(xValues: NDArray, solutionResult: NDArray, solutionLabel: str, solutionType: str) -> None:
    """`plotGraph` computes the simulation graph values."""
    
    # Obtaining the negative x half (from x -L to 0) of the function
    # This is only possible because of the fact that all solutions to the well potential are symmetrical
    xNegativeValues = xValues[:0:-1] * -1

    yNegativeValues: NDArray
    if solutionType == "even":
        yNegativeValues = solutionResult[:0:-1] * 1
    else:
        yNegativeValues = solutionResult[:0:-1] * -1

    # Combining the values to get the full function values from -L to L
    xAxis = np.concatenate((xNegativeValues, xValues) )
    yAxis = np.concatenate((yNegativeValues, solutionResult) )

    plt.plot(xAxis, yAxis, label=solutionLabel)

    # Get all major plot ticks based on overall x axis 
    indices = np.linspace(0, xAxis.size-1, 5, dtype=int)
    tickValues = np.round(xAxis[indices], 2)

    ax = plt.gca()
    ax.set_xlim(tickValues[0], tickValues[-1]) # Enforce hard limits for plot from -L ro L
    ax.set_xticks(tickValues) # Show major tick marks

# Display the graph to screen.
def displayGraph() -> None:
    """`displayGraph` shows the computed simulation graph to the screen."""

    plt.legend()
    
    plt.show()

# Save graph to file.
def saveGraph(outputPath: str = "data", graphName: str = "new-graph") -> None:
    """`saveGraph` saves the computed simulation graph to `outputPath/graphName`."""

    # Check if output path exists
    os.makedirs(outputPath, exist_ok=True)

    filename: str = os.path.join(outputPath, "%s.png" % graphName)
    
    plt.savefig(filename)