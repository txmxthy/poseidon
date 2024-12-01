import json
from typing import List
from tqdm import tqdm
import os

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

        # Ensure output directory exists with proper permissions
        output_dir = os.path.dirname(self.output_path)
        ensure_output_dir(output_dir)

        try:
            print(f"\nWriting output to {self.output_path}...")
            # First write to a temporary file
            temp_path = f"{self.output_path}.tmp"
            with open(temp_path, 'w') as f:
                json.dump(geojson, f, indent=2)

            # Set permissions on the temporary file
            os.chmod(temp_path, 0o666)

            # Rename temp file to final file (atomic operation)
            os.replace(temp_path, self.output_path)

        except PermissionError as e:
            print(f"\nPermission error when writing output. Try running:\n")
            print(f"sudo chown $USER {self.output_path}")
            print(f"chmod 666 {self.output_path}")
            raise
