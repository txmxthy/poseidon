import json
from typing import List
from tqdm import tqdm

from ..models.position import Position
from ..utils.file import ensure_output_dir
from ..utils.progress import GEOJSON_CREATOR


class GeoJSONExporter:
    """Exports vessel stops to GeoJSON format."""

    def __init__(self, output_path: str):
        self.output_path = output_path

    def export(self, stops: List[Position]) -> None:
        """Create GeoJSON output file from list of stops."""
        features = []

        with tqdm(stops, **GEOJSON_CREATOR) as pbar:
            for stop in pbar:
                features.append(stop.to_dict())

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        # Ensure output directory exists
        ensure_output_dir(self.output_path)

        print(f"\nWriting output to {self.output_path}...")
        with open(self.output_path, 'w') as f:
            json.dump(geojson, f, indent=2)