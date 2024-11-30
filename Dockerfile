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

# Set the entrypoint to python
ENTRYPOINT ["python"]

# Default command is the module name, but can be overridden
CMD ["-m", "vessel_tracker.vessel_tracker"]