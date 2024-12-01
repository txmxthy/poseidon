"""Core processing functionality with performance profiling."""
from typing import Generator, List
import os

from .processor import MessageProcessor
from .analyzer import VesselAnalyzer
from .exporter import GeoJSONExporter
from vessel_tracker.models import Position
from ..utils.profiling import profiler

def process_vessel_data(
    input_path: str,
    output_path: str,
    min_stop_duration: int = 3600,
    chunk_size: int = 100000,
    max_workers: int = None
) -> None:
    """Main function to process vessel data and identify stops."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print(f"\nProcessing input file: {input_path}")
    print(f"Output will be written to: {output_path}\n")

    # Start detailed profiling
    profiler.start_profiling()

    try:
        # Process messages
        with profiler.profile_section("message_processing"):
            processor = MessageProcessor(input_path, chunk_size=chunk_size, max_workers=max_workers)
            positions = processor.process_messages()

        # Analyze vessel stops
        with profiler.profile_section("vessel_analysis"):
            analyzer = VesselAnalyzer(min_duration=min_stop_duration)
            analyzer.group_positions(positions)
            stops = analyzer.find_stops()

        # Export results
        with profiler.profile_section("geojson_export"):
            exporter = GeoJSONExporter(output_path)
            exporter.export(stops)

        print(f"\nProcessing complete. Found {len(stops):,} stops.")

    finally:
        # Stop profiling and show results
        profiler.stop_profiling()
        profiler.print_metrics()