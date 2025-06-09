# Quantum Eigen-State Simulations

This collection of simulations implements finite-difference solutions to the one-dimensional, time-independent Schrödinger equation for a variety of bound‐state potentials. The goal is to compare numerical eigenvalues and eigenfunctions against known theoretical results and to explore how different potentials influence the spectrum of allowed energy levels.

## Objectives

- **Compute bound-state energies and wavefunctions** for a variety of analytic potentials.  
- **Compare numerical results** against known analytic values (where available).
- **Explore parameter dependence** (well depth, oscillator frequency, Morse parameter λ).

- Main project:
  Harmonic Oscialltor Potential
  (The other projects were also implemented to some degree)

## Structure

1. **`simulations/`**  
    * `well/` - subdirectory containing well potential simulation.
        
        * `infinite/` - subdirectory containing the infinite well potential simulation.
        
        * `finite/` - subdirectory containing the finite well potential simulation.

    * `harmonic/` - subdirectory containing the harmonic oscillator potential simulation.

    * `morse/` - subdirectory containing the symmetrized morse potential simulation (NOT IMPLEMENTED YET).

2. **`util/`**  
    Contains all necessary tools used throughout the simulations.
    Most notably:

    * `Simulation` - object class used to initialize a new simulation. Can be used with default initialisation, but for more accurate results should be inherited and made into a specific simulation child object class.

    * `ModelSystem` - object class used to initialize a new simulation model system. Meaning that it contains the system of model ODEs that are solved during the simulation. Should always be inherited and made into a  specific child model system i.e. InfiniteWellPotential, FiniteWellPotential...

    Besides these, everything else can be run per user basis, but for simplicity helper scripts are provided:

    * `solveSimulation` - solves the system of ODEs in simulation.

    * `bracketSimulation` - brackets and solves the system of ODEs in simulation.

For further detials, each subfolder contains its own README, source code, sample plots, and parameter definitions.

## Requirements

- Python 3.8 or later  
- NumPy  
- SciPy  
- Matplotlib

For simplicity requirements can be achived by running (NOT IMPLEMENTED YET):

```bash
make update
```

which installs and updated all neccessary system packages for the simulation.

## Usage

From project root directory run the specified makefile simulation command:

1. **Infinite Well SImulation:**

```bash
make infinite
```

2. **Finite Well Simulation:**

```bash
make finite
```

3. **Harmonic Oscillator Simulation:**

```bash
make harmonic
```

4. **Morse Symmetrized (NOT IMPLEMENTED YET):**
    
```bash
make morse
```

* To clean any previous simulation data:

```bash
make clean
```
