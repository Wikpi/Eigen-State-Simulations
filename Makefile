.PHONY: all infinite finite clean

all: infinite finite harmonic morse

infinite:
	@echo "Running Infinite Well Simulation..."
	python3 -m simulations.well-potential.infinite.main

finite:
	@echo "Running Finite Well Simulation..."
	python3 -m simulations.well-potential.finite.main

harmonic:
	@echo "Running Harmonic Oscillator Potential Simulation..."
	python3 -m simulations.harmonic-oscillator.main

morse:
	@echo "Running Morse Potential Simulation..."
	python3 -m simulations.morse.main

clean: clean-data clean-trash

clean-data:
	@echo "Cleaning simulation data directories..."
	rm -rf simulations/well-potential/infinite/data/
	rm -rf simulations/well-potential/finite/data/
	rm -rf simulations/harmonic-oscillator/data/

clean-trash:
	@echo "Cleaning project tash..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "Available make targets:"
	@echo "  make infinite     - Run Infinite Well Simulation"
	@echo "  make finite       - Run Finite Well Simulation"
	@echo "  make harmonic     - Run Harmonic Oscillator Potential Simulation"
	@echo "  make morse        - Run Morse Potential Simulation"
	@echo "  make clean        - Remove project trash"
	@echo "  make clean-plots  - Remove generated simulation data"
	@echo "  make all          - Run all simulations"