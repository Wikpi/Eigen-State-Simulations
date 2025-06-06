# from utils.core import Well
import numpy as np
from scipy.constants import pi
from scipy.integrate import odeint
import math as math
import matplotlib.pyplot as plt

# Base class used for infinite well simulation
# class InfiniteWell(Well):
#     def __init__(self):
#         return

# models returns the required model function references used in the simulation.
def models(y, x, epsilon) -> list:
    psi, dpsi = y # psi and psi derivative

    return [dpsi, -pi**2 * epsilon * psi]

# getInitialConditions gets initial epsilon values and determines what solution it should be.
def getInitialConditions(epsilon: float) -> list:
    nEstimate = round(math.sqrt(epsilon))
    if nEstimate % 2 == 1:
        return [1.0, 0.0]  # even solution
    else:
        return [0.0, 1.0]  # odd solution

# solve gets initial epsilon value and solves the ode system based on axisX.
def solve(epsilon: float, axisX: list) -> float:
    initial: list = getInitialConditions(epsilon)

    solution = odeint(models, initial, axisX, args=(epsilon,))

    return solution[:, 0]

# Good enough approximation
approximation: float = 1e-6

def main() -> None:
    # Using bracketing method predict the ground state energy

    # Initial epsilon predictions
    epsilonHigh: float = 0.8
    epsilonLow: float = 1.1

    # From 0 to 0.5 at 0.005 step
    axisX: list = np.linspace(0, 0.5, 40)

    # The amount of times to iterate to increase approximatation of prediction
    iterationCtx: int = 19

    for i in range(iterationCtx):
        # If prediction gap is already smaller than 1e-6 then its good enough
        if abs(epsilonHigh - epsilonLow) < approximation:
            break

        # Midpoint in the prediction gap - approximation
        epsilonMid: float = (epsilonHigh + epsilonLow) / 2
        
        solutionLow: list = solve(epsilonLow, axisX)
        solutionHigh: list = solve(epsilonHigh, axisX)
        solutionMid: list = solve(epsilonMid, axisX)
        
        # Depending on what solution is at the wall (where lim x -> 0.5 and function 'vanishes'), adapt the bounding prediction limits
        if np.sign(solutionMid[-1]) == np.sign(solutionHigh[-1]):
            epsilonHigh = epsilonMid
        else:
            epsilonLow = epsilonMid

    # Final state energy - the midpoint in the accurate prediction gap
    stateEnergy: float = (epsilonHigh + epsilonLow) / 2

    print("Ground state energy approximated to %e" % stateEnergy)

    plt.plot(axisX, solutionLow, label=f"ε_low", linestyle='--')
    plt.plot(axisX, solutionHigh, label=f"ε_high", linestyle='-.')

    plt.title("Ground State Energy")
    plt.xlabel("ξ")
    plt.ylabel("ψ(ξ)")
    plt.legend()
    plt.grid(True)
    plt.show()

main()