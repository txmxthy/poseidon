FROM python:3.10-slim

WORKDIR /app

# Copy package files
COPY setup.py pyproject.toml ./
COPY vessel_tracker/ vessel_tracker/
COPY tests/ tests/
COPY requirements.txt .

# Install dependencies and package
RUN pip install -r requirements.txt && \
    pip install .

# Use CMD instead of ENTRYPOINT for more flexibility (let us use tests, etc.)
CMD ["python", "-m", "vessel_tracker.vessel_tracker"]