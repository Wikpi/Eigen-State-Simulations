import util.simulation as sm
from scipy.constants import pi

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
        self.dataPath: str = "simulations/infinite/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon: float) -> list:
        """Infinite Well Potential model system structure."""

        y1, y2 = y # psi and psi derivative

        return [y2, -pi**2 * epsilon * y1] # dy1dx and dy2dx


def main() -> None:
    model: InfiniteWellPotential = InfiniteWellPotential()

    simulation: sm.Simulation = sm.Simulation("%s Solve Simulation" % model.label)
    simulation.modifyGrid(0, 0.5, 0.005, "Position x/L (Dimensionless)", "Wavefunction values")
    
    epsilonList: list = [1, 4, 9, 16]

    # Solve system of ODEs for epsilon list
    sm.solveSimulation(simulation, model, epsilonList, True)

    ### Update the model to simulation energy state finding using bracketing method

    simulation.title = "%s Bracket Simulation" % model.label

    model.iterationCount = 25
    model.approximatation = 1e-6

    bracketList: list = [(0.8, 1.1)]

    # Bracket energy state
    sm.bracketSimulation(simulation, model, bracketList, True)

    print("Done running the %s simulation." % model.label)

    return

main()