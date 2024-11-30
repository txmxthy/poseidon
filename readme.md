# From the project root
pytest tests/

# With coverage report
pytest --cov=src tests/

# Build
docker build -t vessel-tracker .

# Run application
docker run -v $(pwd)/data:/data vessel-tracker /data/input/sample.json.gz /data/output/output.geojson

# Run tests in container
docker run vessel-tracker pytest tests/