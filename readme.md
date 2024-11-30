# Vessel Tracker

A Python application for analyzing vessel AIS data to identify vessel stops.

<h3 align="center">
  <img src="images/Screenshot%202024-11-30%20201642.png" alt="Screenshot of Boat locations" style="width:800px; height:auto;">
</h3>

- I'm going to do a bit of performance optimization, the current base speed is around 180k/s to 220k/s depending on docker/local run for me.
- Future work: 
  - Speedup, 
  - Ensure consistency with definition of "stopped" (trying to get correct count)
  - Animated map of vessel movement
  - Could always do more tests


## Project Structure

```
vessel_tracker/
├── vessel_tracker/          # Main package
│   ├── __init__.py         # Package initialization and version
│   ├── cli.py              # Command line interface
│   ├── core/               # Core processing logic
│   │   ├── __init__.py
│   │   ├── analyzer.py     # Vessel stop analysis
│   │   ├── exporter.py     # GeoJSON export
│   │   └── processor.py    # Message processing
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   └── position.py     # Position data class
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── file.py         # File operations
│       ├── geo.py          # Geographic calculations
│       ├── parsing.py      # Message parsing
│       └── progress.py     # Progress bars
├── tests/                  # Test suite
├── data/                   # Data directory
│   ├── input/             # Input data files
│   └── output/            # Generated output files
├── Makefile               # Build and test automation
└── README.md              # This file
```

## Prerequisites

- Python 3.10 or higher
- Docker (optional)
- Make (optional)

## Quick Start

1. Set up development environment:
```bash
make dev-setup
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Process the sample data:
```bash
# Using Make (recommended)
make run-sample      # Run locally
make run-sample-docker  # Run using Docker

# Direct usage
python -m vessel_tracker.cli data/input/sample.json.gz data/output/output.geojson

# Using Docker directly
docker run -v $(pwd)/data:/data vessel-tracker \
    -m vessel_tracker.cli /data/input/sample.json.gz /data/output/output.geojson
```

3. Process your own data:
```bash
# Local execution
python -m vessel_tracker.cli path/to/input.json.gz path/to/output.geojson

# With custom stop duration (in seconds, default is 3600)
python -m vessel_tracker.cli --min-duration 7200 path/to/input.json.gz path/to/output.geojson
```

## Development Commands

All common operations are available through the Makefile:

```bash
# Show all available commands
make help

# Development Setup
make dev-setup      # Create venv and install dependencies
make install        # Install package in development mode

# Running
make run-sample     # Process sample data locally
make run-sample-docker  # Process sample data using Docker

# Testing
make dev-test       # Run tests locally
make dev-test-cov   # Run tests with coverage locally

# Code Quality
make lint           # Run pylint
make format         # Format code with black and isort
make check          # Check code style

# Docker Operations
make build          # Build Docker image
make test          # Run tests in Docker
make test-cov      # Run tests with coverage in Docker

# Cleanup
make clean         # Remove temporary files and caches
```

## Package Components

### Core Modules
- `core.processor`: Handles AIS message processing
- `core.analyzer`: Implements vessel stop detection
- `core.exporter`: Manages GeoJSON output generation

### Utilities
- `utils.geo`: Geographic calculations
- `utils.file`: File handling operations
- `utils.parsing`: Message parsing
- `utils.progress`: Progress bar configurations

### Models
- `models.position`: Position data model

## Testing

```bash
# Run all tests
make dev-test

# Run with coverage report
make dev-test-cov

# Run specific test file
pytest tests/test_analyzer.py
```

## Data Formats

### Input (AIS Messages)
```json
{
    "Message": {
        "MessageID": 18,
        "UserID": "123456789",
        "Latitude": 51.5074,
        "Longitude": -0.1278
    },
    "UTCTimeStamp": 1588636800
}
```

### Output (GeoJSON)
```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-0.1278, 51.5074]
            },
            "properties": {
                "mmsi": "123456789",
                "timestamp": 1588636800,
                "datetime": "2020-05-05T00:00:00Z"
            }
        }
    ]
}
```

## Troubleshooting

### Common Issues

1. Input file not found:
```bash
# Ensure you're running from the project root directory
cd /path/to/vessel_tracker
# Use relative paths from project root
python -m vessel_tracker.cli data/input/sample.json.gz data/output/output.geojson
```

2. Tests not running:
```bash
# Ensure you're in the project root
cd vessel_tracker
# Install package in editable mode
make install
```

3. Docker volume mounting issues:
```bash
# Ensure you're running from the project root
cd /path/to/vessel_tracker
# Use absolute paths for Docker volume
docker run -v $(pwd)/data:/data vessel-tracker ...
```

4. Permission issues:
```bash
# Fix file permissions
chmod +x venv/bin/activate
```