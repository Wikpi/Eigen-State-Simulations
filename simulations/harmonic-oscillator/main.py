import math as math
import numpy as np
from numpy.typing import NDArray
import util.simulation as sm
import util.solution as sl
import util.core as core

debug: bool = False

class HarmonicOscillator(sm.ModelSystem):
    """Base model system object class. Adapted to model the Harmonic Oscillator as per project description

       Class variables:
        #   label: str              - name of the model system
        #   initialConditions: dict - model system initial conditions
        #   type: str               - type of model simulation: solve or bracket
        #   dataPath: str           - path to simulation data
    """

    #Harmonic Oscillator model constructor
    def __init__(self) -> None:
        self.label: str = "Harmonic Oscillator"
        self.type: str = "solve"
        self.dataPath: str = "simulations/harmonic/data"
        self.initialConditions: dict = {
            "odd": [0, 1],
            "even": [1, 0]
        }

    @staticmethod # Just instruct the class to not inject 'self' as function argument
    def system(y, x, epsilon) -> list:

        y1 , y2 = y #unpacking psi and psi'

        return[y2, (0.5 * (x**2) - epsilon) * y1] #returns rhs values of the system differential equations for psi' and psi''
    
def findSolutions(model: sm.ModelSystem, xValues: NDArray, nSolutions: int = 1, iterationLimit: int = 32) -> dict:
    ''' `findSolutions` finds a required number of solutions for a given `model` over a range of `xValues`\n
        and returns them as a dictionary containing the epsilon values paired with the solution yValues
    '''
    #specifying initial variables for the solution search loop
    resultSolutions: dict = {}
    nFoundSolutions: int = 0
    bracketList: list = [(0,1)]
    nearZero: float = 1e-5 #Decreasing this further may lead to some solutions not being recognised by the code. This is due to the limitation of the numerical method.
    currentIterations: int = 0

    while nFoundSolutions <= nSolutions:

        #applying the bracketEnergyState function to look for potential solutions within the limit
        bracketSolution: sl.Solution = core.bracketEnergyState(model, xValues, bracketList)[0] #The function returns a list of sl.Solution objects, so [0] simply extracts the first and only solution

        #creating a temporary list to edit the brack values
        bracketListTemp: list = list(bracketList[0])

        #checking if the bracket method leads to a valid solution by checking if it tends to 0
        if math.fabs(bracketSolution.result[-1]) < nearZero: #This method of checking may not work as intended for different nearZero values
            
            #printing the details of each found solution for debugging purposes
            if debug:
                print("Current Iteration %d \n bracket value: %r \n solution at endpoint: %f"%(currentIterations, bracketListTemp, bracketSolution.result[-1]))
            
            #updating the solution counter
            nFoundSolutions += 1
            
            #storing the found solution
            resultSolutions[bracketSolution.epsilon] = bracketSolution

            #updates the bracket to continue looking for further solutions
            
            bracketListTemp[0] = bracketSolution.epsilon + 0.1 #adding 0.1 prevents code gettign stuck on the same solution

            #preventing the code getting stuck on the same solution due to the bracket having the same limits
            if bracketListTemp[0] == bracketListTemp[1]:
                bracketListTemp[1] += 1

        else:
            
            #updating the bracket list
            bracketListTemp[1] += 1
        
        #updating the bracketList with the new brackets from bracketListTemp
        bracketList = [tuple(bracketListTemp)]

        #preventing infinite loops by limiting iterations
        currentIterations += 1
        if  currentIterations >= iterationLimit:
            print("Only %d solutions found after %d iterations"%(nFoundSolutions, currentIterations))
            break

    #printing success msg if the required number of solutions is found within the iteration limit
    else:
        print("Solutions successfully found within %d iterations, at epsilon values: "%currentIterations, list(resultSolutions.keys()))

    return resultSolutions

def main() -> None:
    
    model : HarmonicOscillator = HarmonicOscillator()

    #specifying the solution search parameters
    nSolutions: int = 5
    xValues = np.linspace(0, 4, int(4/0.005))
    iterationLimit = 32

    simulation: sm.Simulation = sm.Simulation(title = "%s bracket simulation: first %d solutions"%(model.label, nSolutions))
    simulation.modifyGrid(0, 4, 0.005, "$Position  \\xi  (Dimensionless)$", "$Wavefunction y_1 Values")

    #obtaining the required solutions
    resultSolutions: dict = findSolutions(model, xValues, nSolutions, iterationLimit)
    resultEpsilons: list = list(resultSolutions.keys())

    #specifying simulation parameters, particularly for the bracketEnergyState() function
    model.iterationCount = 32
    model.approximation = 1e-16

    sm.runSimulation(simulation, model, resultEpsilons, True)

    print("Done running the %s simulation." % model.label)

    return

main()   
