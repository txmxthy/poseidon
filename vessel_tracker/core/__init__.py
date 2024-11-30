"""Core processing functionality."""
from typing import Generator, List
import os

# Relative imports for internal core modules
from .processor import MessageProcessor
from .analyzer import VesselAnalyzer
from .exporter import GeoJSONExporter

# Absolute imports for external modules
from vessel_tracker.models import Position


def process_vessel_data(input_path: str, output_path: str, min_stop_duration: int = 3600) -> None:
    """Main function to process vessel data and identify stops."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"\nProcessing input file: {input_path}")
    print(f"Output will be written to: {output_path}\n")

    # Process messages
    processor = MessageProcessor(input_path)
    positions = processor.process_messages()

    # Analyze vessel stops
    analyzer = VesselAnalyzer(min_duration=min_stop_duration)
    analyzer.group_positions(positions)
    stops = analyzer.find_stops()

    # Export results
    exporter = GeoJSONExporter(output_path)
    exporter.export(stops)

    print(f"\nProcessing complete. Found {len(stops):,} stops.")


__all__ = [
    'MessageProcessor',
    'VesselAnalyzer',
    'GeoJSONExporter',
    'process_vessel_data',
    'Position'
]
