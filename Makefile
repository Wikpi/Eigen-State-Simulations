.PHONY: all infinite finite clean

infinite:
	@echo "Running Infinite Well Simulation..."
	python3 -m simulations.infinite.main

finite:
	@echo "Running Finite Well Simulation..."
	python3 -m simulations.finite.main

harmonic:
	@echo "Running Harmonic Oscillator Simulation..."
	python3 -m simulations.harmonic-oscillator.main

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete