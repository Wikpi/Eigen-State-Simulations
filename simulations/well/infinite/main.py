# Package imports
from scipy.constants import pi
import math

# Custom imports
import util.simulation as sm
import util.core as core
import util.bracket as br

class InfiniteWellPotential(sm.ModelSystem):
    """Base model system object class. Should be inherited and adapted per simulation.

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   dataPath: str           - path to simulation data
    """

    # Infinite well potential model constructor
    def __init__(self) -> None:
        self.label: str = "Infinite Well Potential"
        self.dataPath: str = "simulations/well/infinite/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon: float) -> list:
        """Infinite Well Potential model system structure."""

        y1, y2 = y # psi and psi derivative

        return [y2, -pi**2 * epsilon * y1] # dy1dx and dy2dx

# Determine the wavefunction type: odd or even.
def checkWavefunctionEvenOdd(epsilon: float) -> str:
    """`checkWavefunctionEvenOdd` determines whether the wavefunction is odd or even.
        This is based on the fact: `epsilon = pow(n, 2)` and if `n` is even the
        wavefunction will be odd, if `n` odd then the wavefunction will be even. 
    """

    if round(math.sqrt(epsilon)) % 2 == 0:
        return "odd"
    else:
        return "even"

initialEpsilons: list = [1, 4, 9, 16]

def main() -> None:
    model: InfiniteWellPotential = InfiniteWellPotential()

    simulation: sm.Simulation = sm.Simulation("%s Solve Simulation" % model.label)
    simulation.modifyGrid(0, 0.5, 0.005, 0.5, "Position x/L (Dimensionless)", "Wavefunction values")
    
    # Initial epsilon list with found data: parity...
    epsilonList: list[core.Epsilon] = []
    
    for epsilon in initialEpsilons:
        parity = checkWavefunctionEvenOdd(epsilon)

        newEpsilon: core.Epsilon = core.Epsilon(epsilon, parity)

        epsilonList.append(newEpsilon)

    # Solve system of ODEs for epsilon list
    sm.solveSimulation(simulation, model, epsilonList, True)

    ### Update the model to simulation energy state finding using bracketing method

    simulation.title = "%s Bracket Simulation" % model.label

    model.iterationCount = 25
    model.approximatation = 1e-6

    bracketList: list[br.Bracket] = [br.Bracket(0.8, 1.1, "even")]

    # Bracket energy state
    sm.bracketSimulation(simulation, model, bracketList, True)

    print("Done running the %s simulation." % model.label)

    return

main()