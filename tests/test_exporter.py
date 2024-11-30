import json
import tempfile
from pathlib import Path
from vessel_tracker.core.exporter import GeoJSONExporter


def test_export_stops(sample_positions):
    """Test exporting stops to GeoJSON."""
    with tempfile.NamedTemporaryFile(suffix='.geojson', delete=False) as tf:
        output_path = Path(tf.name)

    try:
        exporter = GeoJSONExporter(str(output_path))
        exporter.export(sample_positions)

        # Verify the output file
        with open(output_path) as f:
            data = json.load(f)

        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == len(sample_positions)

        feature = data["features"][0]
        assert feature["type"] == "Feature"
        assert feature["geometry"]["type"] == "Point"
        assert len(feature["geometry"]["coordinates"]) == 2
        assert "mmsi" in feature["properties"]
        assert "timestamp" in feature["properties"]
        assert "datetime" in feature["properties"]
    finally:
        output_path.unlink()


def test_export_empty_stops():
    """Test exporting empty stop list."""
    with tempfile.NamedTemporaryFile(suffix='.geojson', delete=False) as tf:
        output_path = Path(tf.name)

    try:
        exporter = GeoJSONExporter(str(output_path))
        exporter.export([])

        with open(output_path) as f:
            data = json.load(f)

        assert data["type"] == "FeatureCollection"
        assert len(data["features"]) == 0
    finally:
        output_path.unlink()
