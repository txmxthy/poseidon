# From the project root
pytest tests/

# With coverage report
pytest --cov=src tests/

# Build
docker build -t vessel-tracker .

# Run application (will use input/output paths as arguments to the python module)
docker run -v $(pwd)/data:/data vessel-tracker -m vessel_tracker.vessel_tracker /data/input/sample.json.gz /data/output/output.geojson

# Run tests (overrides the default CMD with pytest command)
docker run vessel-tracker -m pytest tests/