# Finite Square Well Simulation

Compute bound-state energies and wavefunctions for a one-dimensional finite square well by numerically integrating the time-independent Schrödinger equation and locating eigenvalues via a bracketing method.

## Description

**Potential**  
V(x) =
    0, for 0 < x < L
    V0, for x ≥ L

**Objective**  
Finding numerical solutions that satisfy the condition of making the wavelength vanish at the well wall.

## Requirements

Python 3.8+  
NumPy  
SciPy  
Matplotlib

## Parameters

--------------- | ----------------------------------- | -------
xMin            | Well integration start              | 0.0
xMax            | well integration end                | 1.5
xStep           | Well integration step               | 0.005
wellWall        | Well wall position                  | 0.5
z0List          | Initial z0 to simulate              | [1, 5, 8, 14]

## Usage

From project root directory run:

```bash
make finite
```

## Output

Computed energies for specified epsilon values.
Optionally plotted.
