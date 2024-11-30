.PHONY: build test test-cov clean dev-setup dev-test dev-test-cov lint format check install run run-sample run-sample-docker ensure-dirs

# Directory setup
ensure-dirs:
	mkdir -p data/input data/output
	chmod 777 data/output

# Run with sample data
run-sample: ensure-dirs
	python -m vessel_tracker.cli data/input/sample.json.gz data/output/output.geojson

# Run with sample data in Docker
run-sample-docker: ensure-dirs
	docker run -v "$(shell pwd)/data:/data" vessel-tracker \
		-m vessel_tracker.cli /data/input/sample.json.gz /data/output/output.geojson

# Docker commands
build:
	docker build -t vessel-tracker .

test: build
	docker run vessel-tracker -m pytest tests/

test-cov: build
	docker run vessel-tracker -m pytest --cov=vessel_tracker --cov-report=term-missing tests/

# Development setup
dev-setup:
	python -m venv venv
	. venv/bin/activate && \
	pip install -r requirements.txt && \
	pip install -e .

# Development commands
install:
	pip install -e .

dev-test:
	pytest tests/

dev-test-cov:
	pytest --cov=vessel_tracker --cov-report=term-missing tests/

# Linting and formatting
lint:
	pylint vessel_tracker tests

format:
	black vessel_tracker tests
	isort vessel_tracker tests

check: lint
	black --check vessel_tracker tests
	isort --check vessel_tracker tests

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".tox" -exec rm -r {} +

# Run application
run:
	python -m vessel_tracker.cli

# Help target
help:
	@echo "Available commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make test           - Run tests in Docker"
	@echo "  make test-cov       - Run tests with coverage in Docker"
	@echo "  make run-sample     - Run the application with sample data"
	@echo "  make run-sample-docker - Run the application with sample data in Docker"
	@echo "  make dev-setup      - Set up development environment"
	@echo "  make install        - Install package in development mode"
	@echo "  make dev-test       - Run tests locally"
	@echo "  make dev-test-cov   - Run tests with coverage locally"
	@echo "  make lint           - Run linter"
	@echo "  make format         - Format code"
	@echo "  make check          - Check code style"
	@echo "  make clean          - Clean up temporary files"
	@echo "  make run            - Run the application"