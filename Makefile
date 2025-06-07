.PHONY: all infinite finite clean

infinite:
	@echo "Running Infinite Well Simulation..."
	python3 -m infinite.main

finite:
	@echo "Running Finite Well Simulation..."
	python3 -m finite.main

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete