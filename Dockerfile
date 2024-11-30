FROM python:3.10-slim

WORKDIR /app

# Copy package files
COPY setup.py pyproject.toml ./
COPY vessel_tracker/ vessel_tracker/
COPY tests/ tests/
COPY requirements.txt .

# Install the package in development mode
RUN pip install -e ".[dev]"

ENTRYPOINT ["python", "-m", "vessel_tracker.vessel_tracker"]
