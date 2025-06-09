# Infinite Square Well Simulation

Compute bound-state energies and wavefunctions for a one-dimensional infinite square well by numerically integrating the time-independent Schrödinger equation and locating eigenvalues via a bracketing method.

## Description

**Potential**  
V(x) =
    0, for 0 < x < L  
    infinite, otherwise

**Objective**  
Finding numerical solutions that satisfy the condition of making the wavelength vanish at the well wall.

## Requirements

Python 3.8+ or later
NumPy  
SciPy  
Matplotlib 

## Parameters

Name            | Description                         | Default
--------------- | ----------------------------------- | -------
xMin            | Well integration start              | 0.0
xMax            | well integration end                | 0.5
xStep           | Well integration step               | 0.005
wellWall        | Well wall position                  | 0.5
initialEpsilons | Initial epsilons to simulate        | [1, 4, 9, 16]
bracketMin      | Min epsilon to bracket ground state | 0.8
bracketMax      | Max epsilon to bracket ground state | 1.1

## Usage

From project root directory run:

```bash
make infinite
```

## Output

Computed energies for specified epsilon values.
Optionally plotted.